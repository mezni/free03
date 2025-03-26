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
FILES=("cdr.go")

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
create_directory "$BASE_DIR/domain/entities"
create_directory "$BASE_DIR/domain/repositories"
create_directory "$BASE_DIR/domain/factories"

# Application Layer
create_directory "$BASE_DIR/application"
#create_directory "$BASE_DIR/application/dtos"
#create_directory "$BASE_DIR/application/mappers"
create_directory "$BASE_DIR/application/services"
create_directory "$BASE_DIR/application/interfaces"

# Infrastructure Layer
create_directory "$BASE_DIR/infrastructure"
create_directory "$BASE_DIR/infrastructure/inmemstore"
#create_directory "$BASE_DIR/infrastructure/boltstore"
#create_directory "$BASE_DIR/infrastructure/filestore"
create_directory "$BASE_DIR/infrastructure/sqlitestore"

# Configs 
create_directory "$BASE_DIR/configs"

# Add files to specific directories
for FILE in "${FILES[@]}"; do
    create_file "$BASE_DIR/domain/entities/$FILE"
    create_file "$BASE_DIR/domain/repositories/$FILE"
    create_file "$BASE_DIR/domain/factories/$FILE"
#    create_file "$BASE_DIR/domain/factories/$FILE"
#    create_file "$BASE_DIR/application/dtos/$FILE"
#    create_file "$BASE_DIR/application/mappers/$FILE"
    create_file "$BASE_DIR/application/services/$FILE"
    create_file "$BASE_DIR/infrastructure/inmemstore/$FILE"
done

go mod init github.com/mezni/wovoka

echo "Scaffold complete."
exit 0
