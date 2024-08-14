#!/bin/bash

# Directory to create
TEST_DIR="/tmp/test_source"
mkdir -p $TEST_DIR

# Target size (e.g., 50GB)
TARGET_SIZE=$((50 * 1024 * 1024 * 1024))  # 50 GB in bytes
CURRENT_SIZE=0

# Create files of various sizes until we reach or exceed the target size
while [ $CURRENT_SIZE -lt $TARGET_SIZE ]; do
    # Random file size between 10MB and 500MB
    FILE_SIZE=$(( (RANDOM % 491520) + 10240 ))  # Size in KB
    FILE_SIZE_BYTES=$(( FILE_SIZE * 1024 ))     # Convert to bytes

    # File name
    FILE_NAME="$TEST_DIR/file_$CURRENT_SIZE.bin"

    # Create a file with random content
    head -c $FILE_SIZE_BYTES </dev/urandom > $FILE_NAME

    # Update current directory size
    CURRENT_SIZE=$((CURRENT_SIZE + FILE_SIZE_BYTES))
done

echo "Directory $TEST_DIR has been created with a total size of $((CURRENT_SIZE / (1024 * 1024 * 1024))) GB"


