CREATE OR REPLACE FUNCTION current_user_id()
RETURNS INTEGER AS $$
DECLARE
    current_user_id INTEGER;
BEGIN
    current_user_id := 1;  
    RETURN current_user_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_charging_station_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_by := current_user_id();  
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_charging_station_timestamp_trigger
BEFORE UPDATE ON charging_stations
FOR EACH ROW
EXECUTE PROCEDURE update_charging_station_timestamp();