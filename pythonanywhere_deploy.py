#!/usr/bin/env python3
"""
PythonAnywhere Deployment Script
Automates pulling latest changes from GitHub and reloading the web app
"""

import subprocess
import sys
import os
from datetime import datetime

REPO_PATH = '/home/RuralITHUB/FARMITHUB'
WSGI_FILE = '/var/www/RuralITHUB_pythonanywhere_com_wsgi.py'
LOG_FILE = '/home/RuralITHUB/deploy.log'

def log_message(msg):
    """Log deployment messages"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {msg}"
    print(log_entry)
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + '\n')

def run_command(cmd, description):
    """Execute shell command and log result"""
    log_message(f"Running: {description}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=REPO_PATH, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            log_message(f"✓ {description} - SUCCESS")
            if result.stdout:
                log_message(f"  Output: {result.stdout.strip()}")
            return True
        else:
            log_message(f"✗ {description} - FAILED")
            if result.stderr:
                log_message(f"  Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        log_message(f"✗ {description} - TIMEOUT")
        return False
    except Exception as e:
        log_message(f"✗ {description} - EXCEPTION: {str(e)}")
        return False

def deploy():
    """Main deployment function"""
    log_message("=" * 60)
    log_message("DEPLOYMENT STARTED")
    log_message("=" * 60)
    
    # Step 1: Fetch latest changes
    if not run_command('git fetch origin', 'Fetch from GitHub'):
        log_message("Deployment aborted: git fetch failed")
        return False
    
    # Step 2: Reset to latest main branch
    if not run_command('git reset --hard origin/main', 'Reset to origin/main'):
        log_message("Deployment aborted: git reset failed")
        return False
    
    # Step 3: Show current commit
    run_command('git log --oneline -1', 'Show current commit')
    
    # Step 4: Reload web app
    try:
        os.utime(WSGI_FILE, None)
            log_message(f"✓ Touched WSGI file: {WSGI_FILE}")
    except Exception as e:
        log_message(f"✗ Failed to touch WSGI file: {str(e)}")
        return False
    
    # Step 5: Wait for reload
    import time
    log_message("Waiting for web app to reload...")
    time.sleep(2)
    log_message("Web app should be reloaded now")
    
    log_message("=" * 60)
    log_message("DEPLOYMENT COMPLETED SUCCESSFULLY")
    log_message("=" * 60)
    log_message(f"Visit: https://agriconnectdashboard-RuralITHUB.pythonanywhere.com")
    return True

if __name__ == '__main__':
    success = deploy()
    sys.exit(0 if success else 1)
