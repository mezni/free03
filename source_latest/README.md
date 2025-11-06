https://download.geofabrik.de/africa/tunisia-latest.osm.pbf

osm2pgsql -d voltwise_db -U postgres --hstore --multi-geometry tunisia-latest.osm.pbf


docker system prune --all --volumes
docker volume rm $(docker volume ls -qf dangling=true)

docker exec -it postgres psql -U postgres -d voltwise_db


https://www.abetterrouteplanner.com/

python3 -m http.server 8080

Ivy Charging Station
Electric vehicle charging station
400 Dundas St E · +1 800-301-1950
Open 24 hours
CCS·100 kW2/2
CHAdeMO·50 kW2/3

reviews 
photos
nearby locations


docker system prune --all --volumes
docker volume rm $(docker volume ls -qf dangling=true)

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

-- Check for data integrity issues
SELECT 
    COUNT(*) as total_stations,
    COUNT(DISTINCT osm_id) as unique_osm_ids,
    SUM(CASE WHEN location IS NULL THEN 1 ELSE 0 END) as null_locations
FROM charging_stations;


-- First, let's check if the materialized view has data
SELECT COUNT(*) FROM mv_charging_stations_geo;

-- If it's empty, refresh it
REFRESH MATERIALIZED VIEW mv_charging_stations_geo;


-- Test basic spatial query without the function
SELECT 
    id,
    name,
    ST_Distance(location, ST_Point(10.2417, 36.8380)::GEOGRAPHY) as distance_m
FROM charging_stations 
WHERE ST_DWithin(location, ST_Point(10.2417, 36.8380)::GEOGRAPHY, 5000)
ORDER BY distance_m
LIMIT 5;

-- Then try the function again
SELECT * FROM find_nearby_stations(36.8380::float, 10.2417::float, 5000, 10);

-- Find stations with fast charging (50kW+)
SELECT 
    id,
    name,
    max_power_kw,
    power_tier,
    available_connector_names,
    total_available_connectors
FROM mv_charging_stations_geo
WHERE max_power_kw >= 50
ORDER BY max_power_kw DESC;




# Find nearby stations
curl "http://localhost:5000/api/v1/stations/nearby?lat=36.8380&lng=10.2417&radius=5000"

curl "http://localhost:5000/api/v1/stations/nearby?lat=36.8380&lng=10.2417&radius=5000" | jq .

# Get station by ID
curl "http://localhost:8080/api/v1/stations/1"

# Get statistics
curl "http://localhost:8080/api/v1/statistics"

# Search stations
curl "http://localhost:8080/api/v1/stations/search?query=mall&min_power=50"

# Export GeoJSON
curl "http://localhost:8080/api/v1/export/geojson"

# Get connector types
curl "http://localhost:8080/api/v1/connectors/types"