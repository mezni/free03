https://download.geofabrik.de/africa/tunisia-latest.osm.pbf

osm2pgsql -d voltwise_db -U postgres --hstore --multi-geometry tunisia-latest.osm.pbf


docker system prune --all --volumes
docker volume rm $(docker volume ls -qf dangling=true)

docker exec -it postgres psql -U postgres -d voltwise_db


https://www.abetterrouteplanner.com/

python3 -m http.server 8080


uvicorn main:app --host 0.0.0.0 --port 8000 --reload



-- Major Tunisian cities coordinates for testing
-- Tunis: POINT(10.1815 36.8065)
-- Sfax: POINT(10.7685 34.7397)  
-- Sousse: POINT(10.6412 35.8288)
-- Kairouan: POINT(10.1000 35.6833)
-- Bizerte: POINT(9.8737 37.2745)
-- Gabès: POINT(10.0833 33.8833)
-- Djerba: POINT(10.8596 33.8089)
-- Hammamet: POINT(10.6167 36.4000)


INSERT INTO charging_stations (osm_id, name, address, location, args, created_by)
VALUES
    (1020250001,'STEG Charging Station - Lac', 'Lac de Tunis, near Tunis City Center', ST_Point(10.2417, 36.8380, 4326),hstore(ARRAY[
                ['amenity', 'charging_station'],
                ['test', 'test']
            ]), current_user_id()),
    (1020250002,'Hotel Golden Tulip El Mechtel', 'Avenue Ouled Haffouz, Tunis', ST_Point(10.2087, 36.8374, 4326), hstore(ARRAY[
                ['amenity', 'charging_station'],
                ['test', 'test']
            ]),current_user_id()),
    (1020250003,'Tunisia Mall Charging Point', 'Les Berges du Lac, Tunis', ST_Point(10.2376, 36.8510, 4326), hstore(ARRAY[
                ['amenity', 'charging_station'],
                ['test', 'test']
            ]),current_user_id()),
    (1020250004,'Energym Charging Station', 'La Goulette, Tunis', ST_Point(10.3135, 36.8185, 4326), hstore(ARRAY[
                ['amenity', 'charging_station'],
                ['test', 'test']
            ]),current_user_id()),
    (1020250005,'The Residence Tunis', 'Gammarth, Tunis', ST_Point(10.3234, 36.9542, 4326), hstore(ARRAY[
                ['amenity', 'charging_station'],
                ['test', 'test']
            ]),current_user_id()),
    (1020250006,'Carrefour Charging Point', 'Marsa, Tunis', ST_Point(10.3247, 36.8782, 4326), hstore(ARRAY[
                ['amenity', 'charging_station'],
                ['test', 'test']
            ]),current_user_id());


chargingStations = [
            {
                name: "STEG Charging Station - Lac",
                coords: [36.8380, 10.2417],
                type: "Fast Charger",
                address: "Lac de Tunis, near Tunis City Center"
            },
            {
                name: "Hotel Golden Tulip El Mechtel",
                coords: [36.8374, 10.2087],
                type: "Type 2",
                address: "Avenue Ouled Haffouz, Tunis"
            },
            {
                name: "Tunisia Mall Charging Point",
                coords: [36.8510, 10.2376],
                type: "Type 2",
                address: "Les Berges du Lac, Tunis"
            },
            {
                name: "Energym Charging Station",
                coords: [36.8185, 10.3135],
                type: "Fast Charger",
                address: "La Goulette, Tunis"
            },
            {
                name: "The Residence Tunis",
                coords: [36.9542, 10.3234],
                type: "Type 2",
                address: "Gammarth, Tunis"
            },
            {
                name: "Carrefour Charging Point",
                coords: [36.8782, 10.3247],
                type: "Type 2",
                address: "Marsa, Tunis"
            }
        ];


-- Find chargers within 10km of a point
SELECT 
    cs.id,
    cs.name,
    cs.operator,
    ST_Distance(cs.location, ST_Point(2.3522, 48.8566)::GEOGRAPHY) as distance_meters,
    COUNT(cc.id) as total_connectors,
    COUNT(cc.id) FILTER (WHERE cc.status = 'available') as available_connectors
FROM charging_stations cs
LEFT JOIN charging_connectors cc ON cs.id = cc.station_id
WHERE 
    cs.is_active = TRUE
    AND ST_DWithin(
        cs.location, 
        ST_Point(35.8245, 10.6346)::GEOGRAPHY, -- Paris coordinates
        10000 -- 10km radius
    )
GROUP BY cs.id, cs.name, cs.operator, cs.location
ORDER BY distance_meters ASC
LIMIT 50;



7R6J+43 Pêcherie, Tunisia
