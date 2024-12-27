#!/bin/bash

# Function to create directories
create_directory() {
    mkdir -p "$1"
    echo "Created: $1"
}

# Function to create a file
create_file() {
    if [ ! -f "$1" ]; then
        touch "$1"
        echo "Created file: $1"
    else
        echo "File already exists: $1"
    fi
}
# Base project directory (hardcoded or customizable within the script)
BASE_DIR="cdrgen"

# List of subcommands for the `cmd` directory
SUBCOMMANDS=("cdrgen" "cdrcfg")

# List of files to add in specific directories
FILES=("network_technology.go" "network_element_type.go" "service_type.go")

# Create the base project directory
create_directory "$BASE_DIR"

# Command Layer
create_directory "$BASE_DIR/cmd"
for SUBCMD in "${SUBCOMMANDS[@]}"; do
    SUBCMD_DIR="$BASE_DIR/cmd/$SUBCMD"
    create_directory "$SUBCMD_DIR"
    create_file "$SUBCMD_DIR/main.go" # Create main.go in each subcommand directory
done

# Domain Layer
ENTITY_DIR="$BASE_DIR/domain/entities"
REPOSITORY_DIR="$BASE_DIR/domain/repositories"
SERVICE_DIR="$BASE_DIR/domain/services"
create_directory "$ENTITY_DIR"
create_directory "$REPOSITORY_DIR"
create_directory "$SERVICE_DIR"

# Application Layer
create_directory "$BASE_DIR/application"
create_directory "$BASE_DIR/application/dto"
create_directory "$BASE_DIR/application/queries"
create_directory "$BASE_DIR/application/commands"

# Infrastructure Layer
BOLTSTORE_DIR="$BASE_DIR/infrastructure/boltstore"
INMEMSTORE_DIR="$BASE_DIR/infrastructure/inmemstore"
create_directory "$BASE_DIR/infrastructure"
create_directory "$BASE_DIR/infrastructure/logger"
create_directory "$BOLTSTORE_DIR"
create_directory "$INMEMSTORE_DIR"

# Configs 
create_directory "$BASE_DIR/configs"

# Add files to specific directories
for FILE in "${FILES[@]}"; do
    create_file "$ENTITY_DIR/$FILE"
    create_file "$REPOSITORY_DIR/$FILE"
    create_file "$SERVICE_DIR/$FILE"
done

go mod init github.com/mezni/wovoka

echo "Scaffold complete."
exit 0
