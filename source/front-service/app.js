// Base URL for API - UPDATED for separate ports
const API_BASE_URL = 'http://localhost:5000/api/v1';

// All your existing JavaScript functions remain the same, just using API_BASE_URL
// Load all stations
async function loadAllStations() {
    try {
        const response = await fetch(`${API_BASE_URL}/stations`);
        const result = await response.json();
        
        if (result.success && result.data) {
            currentStations = result.data;
            displayStationsOnMap(currentStations);
            updateStationList(currentStations);
        }
    } catch (error) {
        console.error('Error loading stations:', error);
        alert('Error loading stations');
    }
}

// Load nearby stations based on map center
async function loadNearbyStations(lat, lng) {
    try {
        const response = await fetch(`${API_BASE_URL}/stations/nearby?lat=${lat}&lng=${lng}&radius=5000&limit=50`);
        const result = await response.json();
        
        if (result.success && result.data) {
            currentStations = result.data;
            displayStationsOnMap(currentStations);
            updateStationList(currentStations);
        }
    } catch (error) {
        console.error('Error loading nearby stations:', error);
    }
}

// Search stations
async function searchStations() {
    const query = document.getElementById('searchInput').value;
    
    try {
        const url = query ? 
            `${API_BASE_URL}/stations/search?query=${encodeURIComponent(query)}` :
            `${API_BASE_URL}/stations`;
            
        const response = await fetch(url);
        const result = await response.json();
        
        if (result.success && result.data) {
            currentStations = result.data;
            displayStationsOnMap(currentStations);
            updateStationList(currentStations);
            
            // Center map on first result if available
            if (currentStations.length > 0 && currentStations[0].latitude && currentStations[0].longitude) {
                map.setView([currentStations[0].latitude, currentStations[0].longitude], 13);
            }
        }
    } catch (error) {
        console.error('Error searching stations:', error);
    }
}

// Show station details
async function showStationDetails(stationId) {
    try {
        const response = await fetch(`${API_BASE_URL}/stations/${stationId}`);
        const result = await response.json();
        
        if (result.success && result.data) {
            const data = result.data;
            const station = data.station;
            const connectors = data.connectors;
            
            const detailsContent = document.getElementById('stationDetailsContent');
            detailsContent.innerHTML = `
                <h2>${station.name}</h2>
                <div class="station-address">${station.address || 'No address available'}</div>
                
                <div class="station-meta">
                    ${station.operator ? `<div><strong>Operator:</strong> ${station.operator}</div>` : ''}
                    ${station.opening_hours ? `<div><strong>Hours:</strong> ${station.opening_hours}</div>` : ''}
                    ${station.fee ? `<div><strong>Fee:</strong> ${station.fee}</div>` : ''}
                    ${station.parking_fee ? `<div><strong>Parking Fee:</strong> ${station.parking_fee}</div>` : ''}
                </div>
                
                <h3>Connectors (${connectors.length})</h3>
                <div class="connector-list">
                    ${connectors.map(connector => `
                        <div class="connector-item ${connector.count_available > 0 ? 'available' : 'unavailable'}">
                            <div><strong>${connector.connector_type}</strong> (${connector.current_type})</div>
                            <div>Power: ${connector.power_kw || 'N/A'} kW</div>
                            <div>Status: ${connector.status}</div>
                            <div>Available: ${connector.count_available}/${connector.count_total}</div>
                        </div>
                    `).join('')}
                </div>
            `;
            
            document.getElementById('stationDetails').classList.remove('hidden');
            
            // Center map on this station
            if (station.latitude && station.longitude) {
                map.setView([station.latitude, station.longitude], 15);
            }
        }
    } catch (error) {
        console.error('Error loading station details:', error);
        alert('Error loading station details');
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/statistics`);
        const result = await response.json();
        
        if (result.success && result.data) {
            const stats = result.data;
            const statsContent = document.getElementById('statsContent');
            
            statsContent.innerHTML = `
                <div class="stat-item">
                    <span>Total Stations:</span>
                    <span class="stat-value">${stats.total_stations || 0}</span>
                </div>
                <div class="stat-item">
                    <span>Total Connectors:</span>
                    <span class="stat-value">${stats.total_connectors || 0}</span>
                </div>
                <div class="stat-item">
                    <span>Available Connectors:</span>
                    <span class="stat-value">${stats.available_connectors || 0}</span>
                </div>
                <div class="stat-item">
                    <span>Average Power:</span>
                    <span class="stat-value">${stats.avg_power_kw ? stats.avg_power_kw + ' kW' : 'N/A'}</span>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Export to GeoJSON
async function exportToGeoJSON() {
    try {
        const response = await fetch(`${API_BASE_URL}/export/geojson`);
        const geojson = await response.json();
        
        // Download as file
        const blob = new Blob([JSON.stringify(geojson, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'charging-stations.geojson';
        a.click();
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error exporting GeoJSON:', error);
        alert('Error exporting data');
    }
}

// Get connector types
async function getConnectorTypes() {
    try {
        const response = await fetch(`${API_BASE_URL}/connectors/types`);
        return await response.json();
    } catch (error) {
        console.error('Error loading connector types:', error);
        return { success: false, data: [] };
    }
}

// Your existing map initialization and other functions remain the same...
let map;
let userMarker;
let stationMarkers = [];
let currentStations = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    loadStatistics();
    loadAllStations();
    
    // Set up event listeners
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchStations();
        }
    });
    
    document.getElementById('connectorFilter').addEventListener('change', filterStations);
    document.getElementById('powerFilter').addEventListener('change', filterStations);
    document.getElementById('availableOnly').addEventListener('change', filterStations);
});

// Initialize Leaflet map
function initializeMap() {
    console.log('Initializing map...');
    
    // Create map container with explicit height
    const mapContainer = document.getElementById('map');
    if (!mapContainer) {
        console.error('Map container not found!');
        return;
    }
    
    // Default to Tunis center
    map = L.map('map').setView([36.8065, 10.1815], 12);
    
    console.log('Map created, adding tiles...');
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Add scale control
    L.control.scale().addTo(map);
    
    // Add click handler for the map
    map.on('click', function(e) {
        console.log('Map clicked at:', e.latlng);
        loadNearbyStations(e.latlng.lat, e.latlng.lng);
    });
    
    // Add load event to ensure map is properly sized
    map.whenReady(function() {
        console.log('Map is ready');
        // Trigger a resize after a short delay to ensure proper rendering
        setTimeout(function() {
            map.invalidateSize();
            console.log('Map size invalidated');
        }, 100);
    });
    
    console.log('Map initialization complete');
}

// Display stations on the map
function displayStationsOnMap(stations) {
    // Clear existing markers
    stationMarkers.forEach(marker => map.removeLayer(marker));
    stationMarkers = [];
    
    stations.forEach(station => {
        if (station.latitude && station.longitude) {
            const marker = L.marker([station.latitude, station.longitude])
                .addTo(map)
                .bindPopup(createStationPopup(station));
            
            marker.on('click', function() {
                showStationDetails(station.id);
            });
            
            stationMarkers.push(marker);
        }
    });
}

// Create popup content for station markers
function createStationPopup(station) {
    const availableStatus = station.has_available_connectors ? 
        '<span style="color: green;">● Available</span>' : 
        '<span style="color: red;">● Busy</span>';
    
    const powerInfo = station.max_power_kw ? 
        `<div>Max Power: <strong>${station.max_power_kw} kW</strong></div>` : 
        '';
    
    return `
        <div class="popup-content">
            <h3>${station.name}</h3>
            <div>${availableStatus}</div>
            ${powerInfo}
            <div>${station.address || ''}</div>
            <button onclick="showStationDetails(${station.id})" 
                    style="margin-top: 10px; padding: 5px 10px; background: #667eea; color: white; border: none; border-radius: 3px; cursor: pointer;">
                View Details
            </button>
        </div>
    `;
}

// Update station list in sidebar
function updateStationList(stations) {
    const stationList = document.getElementById('stationList');
    
    if (stations.length === 0) {
        stationList.innerHTML = '<p>No stations found</p>';
        return;
    }
    
    stationList.innerHTML = stations.map(station => `
        <div class="station-item ${station.has_available_connectors ? 'available' : 'unavailable'}" 
             onclick="showStationDetails(${station.id})">
            <div class="station-name">${station.name}</div>
            <div class="station-info">
                <div>${station.address || ''}</div>
                <div>
                    ${station.max_power_kw ? `<span class="power-badge">${station.max_power_kw}kW</span>` : ''}
                    ${station.has_available_connectors ? '<span style="color: green;">● Available</span>' : '<span style="color: red;">● Busy</span>'}
                </div>
                <div>${station.distance_meters ? `Distance: ${(station.distance_meters / 1000).toFixed(1)}km` : ''}</div>
            </div>
        </div>
    `).join('');
}

// Filter stations based on selected criteria
function filterStations() {
    const connectorFilter = document.getElementById('connectorFilter').value;
    const powerFilter = document.getElementById('powerFilter').value;
    const availableOnly = document.getElementById('availableOnly').checked;
    
    let filteredStations = [...currentStations];
    
    if (connectorFilter) {
        // This would need additional API call or client-side filtering
        // For now, we'll just show all and indicate this needs backend support
        console.log('Connector filter selected:', connectorFilter);
    }
    
    if (powerFilter) {
        const minPower = parseInt(powerFilter);
        filteredStations = filteredStations.filter(station => 
            station.max_power_kw && parseFloat(station.max_power_kw) >= minPower
        );
    }
    
    if (availableOnly) {
        filteredStations = filteredStations.filter(station => 
            station.has_available_connectors
        );
    }
    
    displayStationsOnMap(filteredStations);
    updateStationList(filteredStations);
}

// Close station details
function closeStationDetails() {
    document.getElementById('stationDetails').classList.add('hidden');
}

// Locate user
function locateMe() {
    if (!navigator.geolocation) {
        alert('Geolocation is not supported by your browser');
        return;
    }
    
    navigator.geolocation.getCurrentPosition(
        position => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            
            // Remove existing user marker
            if (userMarker) {
                map.removeLayer(userMarker);
            }
            
            // Add user marker
            userMarker = L.marker([lat, lng])
                .addTo(map)
                .bindPopup('Your location')
                .openPopup();
            
            // Center map on user
            map.setView([lat, lng], 14);
            
            // Load nearby stations
            loadNearbyStations(lat, lng);
        },
        error => {
            alert('Unable to get your location: ' + error.message);
        }
    );
}