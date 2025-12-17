#!/bin/bash

# PythonAnywhere Deployment Script
# Usage: ./deploy.sh

REPO_PATH="/home/uma2003b/FARMITHUB"
WSGI_FILE="/var/www/uma2003b_pythonanywhere_com_wsgi.py"
LOG_FILE="/home/uma2003b/deploy.log"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_message() {
    local msg="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $msg" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}✓ $1${NC}" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}✗ $1${NC}" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${YELLOW}ℹ $1${NC}" | tee -a "$LOG_FILE"
}

# Main deployment
main() {
    log_message "============================================================"
    log_message "DEPLOYMENT STARTED"
    log_message "============================================================"
    
    # Check if repo exists
    if [ ! -d "$REPO_PATH" ]; then
        log_error "Repository not found at $REPO_PATH"
        return 1
    fi
    
    cd "$REPO_PATH" || return 1
    
    # Step 1: Fetch latest changes
    log_info "Fetching latest changes from GitHub..."
    if git fetch origin; then
        log_success "Git fetch completed"
    else
        log_error "Git fetch failed"
        return 1
    fi
    
    # Step 2: Reset to latest main branch
    log_info "Resetting to origin/main..."
    if git reset --hard origin/main; then
        log_success "Git reset completed"
    else
        log_error "Git reset failed"
        return 1
    fi
    
    # Step 3: Show current commit
    log_info "Current commit:"
    git log --oneline -1 | tee -a "$LOG_FILE"
    
    # Step 4: Reload web app
    log_info "Reloading web app..."
    if touch "$WSGI_FILE"; then
        log_success "WSGI file touched - web app reloading"
    else
        log_error "Failed to touch WSGI file"
        return 1
    fi
    
    log_message "============================================================"
    log_success "DEPLOYMENT COMPLETED SUCCESSFULLY"
    log_message "============================================================"
    return 0
}

main
exit $?
