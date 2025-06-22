#!/bin/bash

# Hyrcania Project - Portable Runner Script
# This script makes it easy to run the project on any machine with Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "Docker is available and running"
}

# Check if Docker Compose is available
check_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker-compose"
    elif docker compose version &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker compose"
    else
        print_error "Docker Compose is not available. Please install Docker Compose."
        exit 1
    fi
    
    print_success "Docker Compose is available"
}

# Create necessary directories
setup_directories() {
    print_status "Setting up directories..."
    
    mkdir -p data/extracted
    mkdir -p output
    
    print_success "Directories created"
}

# Build the Docker image
build_image() {
    print_status "Building Docker image..."
    
    if [ "$DOCKER_COMPOSE_CMD" = "docker-compose" ]; then
        docker-compose build --no-cache
    else
        docker compose build --no-cache
    fi
    
    print_success "Docker image built successfully"
}

# Start the services
start_services() {
    print_status "Starting services..."
    
    if [ "$DOCKER_COMPOSE_CMD" = "docker-compose" ]; then
        docker-compose up -d
    else
        docker compose up -d
    fi
    
    print_success "Services started successfully"
}

# Show status
show_status() {
    print_status "Checking service status..."
    
    if [ "$DOCKER_COMPOSE_CMD" = "docker-compose" ]; then
        docker-compose ps
    else
        docker compose ps
    fi
    
    echo ""
    print_success "Jupyter Lab is available at: http://localhost:8888"
    print_success "Jupyter Notebook is available at: http://localhost:8889 (if using notebook profile)"
}

# Stop services
stop_services() {
    print_status "Stopping services..."
    
    if [ "$DOCKER_COMPOSE_CMD" = "docker-compose" ]; then
        docker-compose down
    else
        docker compose down
    fi
    
    print_success "Services stopped"
}

# Show logs
show_logs() {
    print_status "Showing logs..."
    
    if [ "$DOCKER_COMPOSE_CMD" = "docker-compose" ]; then
        docker-compose logs -f
    else
        docker compose logs -f
    fi
}

# Clean up
cleanup() {
    print_status "Cleaning up..."
    
    if [ "$DOCKER_COMPOSE_CMD" = "docker-compose" ]; then
        docker-compose down --rmi all --volumes --remove-orphans
    else
        docker compose down --rmi all --volumes --remove-orphans
    fi
    
    print_success "Cleanup completed"
}

# Show help
show_help() {
    echo "Hyrcania Project - Portable Runner Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     - Build and start the services (default)"
    echo "  stop      - Stop the services"
    echo "  restart   - Restart the services"
    echo "  status    - Show service status"
    echo "  logs      - Show service logs"
    echo "  build     - Build the Docker image"
    echo "  cleanup   - Stop services and remove images/volumes"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start        # Start the project"
    echo "  $0 stop         # Stop the project"
    echo "  $0 restart      # Restart the project"
    echo "  $0 logs         # View logs"
    echo ""
    echo "After starting, access Jupyter Lab at: http://localhost:8888"
}

# Main script logic
main() {
    case "${1:-start}" in
        start)
            check_docker
            check_docker_compose
            setup_directories
            build_image
            start_services
            show_status
            ;;
        stop)
            stop_services
            ;;
        restart)
            stop_services
            sleep 2
            start_services
            show_status
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        build)
            check_docker
            check_docker_compose
            build_image
            ;;
        cleanup)
            cleanup
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@" 