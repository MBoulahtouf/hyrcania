#!/bin/bash

# Hyrcania Project - Data Backup Script
# This script helps backup and restore project data for portability

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

# Default backup directory
BACKUP_DIR="hyrcania_backup_$(date +%Y%m%d_%H%M%S)"

# Create backup
create_backup() {
    print_status "Creating backup..."
    
    # Create backup directory
    mkdir -p "$BACKUP_DIR"
    
    # Copy essential files
    print_status "Copying project files..."
    cp -r data "$BACKUP_DIR/"
    cp -r output "$BACKUP_DIR/" 2>/dev/null || print_warning "No output directory found"
    cp visu.ipynb "$BACKUP_DIR/"
    cp pyproject.toml "$BACKUP_DIR/"
    cp poetry.lock "$BACKUP_DIR/"
    cp README.md "$BACKUP_DIR/"
    cp Dockerfile "$BACKUP_DIR/"
    cp docker-compose.yml "$BACKUP_DIR/"
    cp run.sh "$BACKUP_DIR/"
    
    # Create backup info file
    cat > "$BACKUP_DIR/backup_info.txt" << EOF
Hyrcania Project Backup
Created: $(date)
Version: $(git describe --tags 2>/dev/null || echo "Unknown")
Data size: $(du -sh data 2>/dev/null | cut -f1 || echo "Unknown")
EOF
    
    # Create compressed archive
    print_status "Creating compressed archive..."
    tar -czf "${BACKUP_DIR}.tar.gz" "$BACKUP_DIR"
    
    # Clean up temporary directory
    rm -rf "$BACKUP_DIR"
    
    print_success "Backup created: ${BACKUP_DIR}.tar.gz"
    print_status "Backup size: $(du -h "${BACKUP_DIR}.tar.gz" | cut -f1)"
}

# Restore backup
restore_backup() {
    local backup_file="$1"
    
    if [ -z "$backup_file" ]; then
        print_error "Please specify a backup file to restore"
        echo "Usage: $0 restore <backup_file.tar.gz>"
        exit 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        print_error "Backup file not found: $backup_file"
        exit 1
    fi
    
    print_status "Restoring backup from: $backup_file"
    
    # Extract backup
    print_status "Extracting backup..."
    tar -xzf "$backup_file"
    
    # Find extracted directory
    local extracted_dir=$(tar -tzf "$backup_file" | head -1 | cut -d'/' -f1)
    
    if [ -z "$extracted_dir" ]; then
        print_error "Could not determine extracted directory"
        exit 1
    fi
    
    # Restore files
    print_status "Restoring files..."
    cp -r "$extracted_dir/data" . 2>/dev/null || print_warning "No data directory in backup"
    cp -r "$extracted_dir/output" . 2>/dev/null || print_warning "No output directory in backup"
    cp "$extracted_dir/visu.ipynb" . 2>/dev/null || print_warning "No visu.ipynb in backup"
    cp "$extracted_dir/pyproject.toml" . 2>/dev/null || print_warning "No pyproject.toml in backup"
    cp "$extracted_dir/poetry.lock" . 2>/dev/null || print_warning "No poetry.lock in backup"
    
    # Clean up extracted directory
    rm -rf "$extracted_dir"
    
    print_success "Backup restored successfully"
}

# List available backups
list_backups() {
    print_status "Available backups:"
    
    if ls hyrcania_backup_*.tar.gz 2>/dev/null; then
        echo ""
        print_status "Backup details:"
        for backup in hyrcania_backup_*.tar.gz; do
            echo "  $backup ($(du -h "$backup" | cut -f1))"
        done
    else
        print_warning "No backup files found"
    fi
}

# Show help
show_help() {
    echo "Hyrcania Project - Data Backup Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  backup    - Create a backup of project data (default)"
    echo "  restore   - Restore project data from backup"
    echo "  list      - List available backups"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 backup                    # Create backup"
    echo "  $0 restore backup.tar.gz     # Restore from backup"
    echo "  $0 list                      # List available backups"
    echo ""
    echo "Backup includes:"
    echo "  - data/ directory"
    echo "  - output/ directory"
    echo "  - visu.ipynb"
    echo "  - pyproject.toml"
    echo "  - poetry.lock"
    echo "  - Project configuration files"
}

# Main script logic
main() {
    case "${1:-backup}" in
        backup)
            create_backup
            ;;
        restore)
            restore_backup "$2"
            ;;
        list)
            list_backups
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