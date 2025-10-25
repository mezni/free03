FROM debian:bookworm-backports

ENV DEBIAN_FRONTEND=noninteractive

# Install osm2pgsql and PostgreSQL client
RUN apt-get update && \
    apt-get install -y \
        curl \
        osm2pgsql/bookworm-backports \
        postgresql-client-15 \
        osmctools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy custom style and import script
ADD ./osm-importer.sh /usr/local/bin/osm-importer.sh
ADD ./custom.style /usr/local/bin/custom.style

RUN chmod +x /usr/local/bin/osm-importer.sh

# Set working directory
WORKDIR /osm

ENTRYPOINT ["/usr/local/bin/osm-importer.sh"]
