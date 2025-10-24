https://download.geofabrik.de/africa/tunisia-latest.osm.pbf

osm2pgsql -d voltwise_db -U postgres --hstore --multi-geometry tunisia-latest.osm.pbf


docker system prune --all --volumes
docker volume rm $(docker volume ls -qf dangling=true)

docker exec -it postgres psql -U postgres -d voltwise_db


https://www.abetterrouteplanner.com/

python3 -m http.server 8080


 uvicorn main:app --host 0.0.0.0 --port 8000 --reload



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
