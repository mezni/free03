#!/bin/bash
set -e

# --- Configurable environment variables ---
export PGHOST=${PGHOST:-postgis}
export PGPORT=${PGPORT:-5432}
export PGUSER=${PGUSER:-postgres}
export PGPASSWORD=${PGPASSWORD:-password}
export PGDATABASE=${PGDATABASE:-ev_db}
export REGION=${REGION:-tunisia}
export DATADIR=${DATADIR:-/osm/data}
export PBF=${PBF:-$DATADIR/${REGION}-latest.osm.pbf}
export STYLE=${STYLE:-/usr/local/bin/custom.style}
HOST=download.geofabrik.de

echo "🗺  Importing OpenStreetMap data"
echo "Database: $PGDATABASE@$PGHOST:$PGPORT"
echo "Region: $REGION"
echo "PBF file: $PBF"

# Wait until PostGIS is available
until pg_isready -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" > /dev/null 2>&1; do
  echo "⏳ Waiting for PostGIS..."
  sleep 3
done
echo "✅ PostGIS is ready."

# Check if already initialized
if psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "SELECT 1 FROM osm2pgsql_properties LIMIT 1;" > /dev/null 2>&1; then
  echo "🔄 Database already initialized — updating data..."
  osm2pgsql-replication update \
    -v \
    --host "$PGHOST" \
    --database "$PGDATABASE" \
    --username "$PGUSER" \
    --port "$PGPORT" \
    -- -k --style "$STYLE" --extra-attributes
else
  echo "🚀 Fresh import starting..."

  # Download PBF if not already present
  if [[ -f "$PBF" ]]; then
    echo "✅ Using existing PBF file: $PBF"
  else
    echo "⬇️  Downloading OSM extract for $REGION..."
    mkdir -p "$(dirname "$PBF")"
    curl -L -o "$PBF" "https://${HOST}/${REGION}-latest.osm.pbf"
  fi

  echo "🧩 Enabling PostGIS & hstore extensions..."
  psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "CREATE EXTENSION IF NOT EXISTS postgis;"
  psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "CREATE EXTENSION IF NOT EXISTS hstore;"

  echo "🛠  Importing data into database..."
  osm2pgsql -v \
    --create \
    --slim \
    --cache 4000 \
    --extra-attributes \
    --style "$STYLE" \
    --host "$PGHOST" \
    --database "$PGDATABASE" \
    --user "$PGUSER" \
    --port "$PGPORT" \
    "$PBF"

  echo "🧭 Initializing replication tracking..."
  osm2pgsql-replication init \
    --host "$PGHOST" \
    --database "$PGDATABASE" \
    --user "$PGUSER" \
    --port "$PGPORT" \
    --osm-file "$PBF"

  echo "✅ Import complete."
fi
