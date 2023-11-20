#!/bin/bash

# Specify the directory containing Dockerfiles
dockerfiles_directory="/home/jm/ml_matchers/DLMatchers/dockers"

# Change to the Dockerfiles directory
cd "${dockerfiles_directory}" || exit

# Get a list of Dockerfile names in the form name.Dockerfile
dockerfile_names=($(find . -type f -name "*.Dockerfile"))

# Build each Dockerfile
for dockerfile in "${dockerfile_names[@]}"; do
    # Extract container name from Dockerfile name
    container_name=$(basename "${dockerfile}" | sed 's/\.Dockerfile//')

    # Build Docker container
    docker build -t "${container_name}" -f "${dockerfile}" .

    echo "Container '${container_name}' built successfully."
done
