#!/bin/bash

# Function to load environment variables from .env file
load_env() {
    if [[ -f .env ]]; then
        export $(grep -v '^#' .env | xargs)
    else
        echo "Error: .env file not found!"
        sleep 2
        exit 1
    fi
}

# Function to start a service
run_services() {
    load_env
    cmd="docker compose -f docker-compose.yaml up -d $@"
    eval $cmd
}

# Function to stop a service
stop_services() {
    echo "Stopping services..."
    docker compose -f docker-compose.yaml stop
}

remove_services() {
    echo "Stopping services..."
    docker compose -f docker-compose.yaml rm -fsv
}

# Function to build all services
build_services() {
    load_env
    cmd="docker compose -f docker-compose.yaml build $@"
    eval $cmd
}

# Main script
command_1=$1
shift
other_commands=$@
case $command_1 in
    "run")
        run_services $other_commands
        ;;
    "build")
        build_services $other_commands
        ;;
    "remove")
        remove_services
        ;;
    "stop")
        stop_services
        ;;
    *)
        echo "Error: Invalid command. Usage: ./start.sh {run|build|stop}"
        sleep 2
        exit 1
        ;;
esac
