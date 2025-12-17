# PythonAnywhere Setup - Next Steps

## Current Status
✅ Repository cloned to `/home/RuralITHUB/FARMITHUB`
⏳ Need to complete configuration

## Step 1: SSH Commands to Run

After entering your password, run these commands:

```bash
# Navigate to repo
cd /home/RuralITHUB/FARMITHUB

# Check if repo is there
ls -la

# Verify git status
git status

# Check current branch
git branch
```

## Step 2: Create Virtual Environment

```bash
# Create virtualenv
mkvirtualenv --python=/usr/bin/python3.10 agriconnect

# Activate it (should auto-activate)
source /home/RuralITHUB/.virtualenvs/agriconnect/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Step 3: Configure WSGI File

Create/Edit `/var/www/RuralITHUB_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

path = '/home/RuralITHUB/FARMITHUB'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

from application import application
```

Command to create:
```bash
cat > /var/www/RuralITHUB_pythonanywhere_com_wsgi.py << 'EOF'
import sys
import os

path = '/home/RuralITHUB/FARMITHUB'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

from application import application
EOF
```

## Step 4: Configure Web App in PythonAnywhere Dashboard

1. Go to: https://www.pythonanywhere.com/user/RuralITHUB/webapps/
2. Click: **agriconnectdashboard-RuralITHUB.pythonanywhere.com**
3. Update settings:
   - **Source code**: `/home/RuralITHUB/FARMITHUB`
   - **Working directory**: `/home/RuralITHUB/FARMITHUB`
   - **WSGI configuration file**: `/var/www/RuralITHUB_pythonanywhere_com_wsgi.py`
   - **Virtualenv**: `/home/RuralITHUB/.virtualenvs/agriconnect`
4. Click: **Reload** button

## Step 5: Verify Deployment

```bash
# Check if files are there
ls -la /home/RuralITHUB/FARMITHUB/application.py
ls -la /home/RuralITHUB/FARMITHUB/templates/main.html

# Check error log
tail -50 /var/log/RuralITHUB_pythonanywhere_com.error.log
```

## Step 6: Test the App

Visit: https://agriconnectdashboard-RuralITHUB.pythonanywhere.com

Should see:
- Landing page with "Grow Your Farm, Grow Your Future"
- Login button
- About link

## Troubleshooting

If app doesn't load:
1. Check error log: `tail -50 /var/log/RuralITHUB_pythonanywhere_com.error.log`
2. Verify WSGI file exists: `cat /var/www/RuralITHUB_pythonanywhere_com_wsgi.py`
3. Check virtualenv: `ls -la /home/RuralITHUB/.virtualenvs/agriconnect/`
4. Reload web app again from dashboard

## Quick Commands Summary

```bash
# SSH in
ssh RuralITHUB@ssh.pythonanywhere.com

# Navigate
cd /home/RuralITHUB/FARMITHUB

# Activate virtualenv
source /home/RuralITHUB/.virtualenvs/agriconnect/bin/activate

# Pull updates
git pull origin main

# Reload app
touch /var/www/RuralITHUB_pythonanywhere_com_wsgi.py

# Check logs
tail -50 /var/log/RuralITHUB_pythonanywhere_com.error.log
```
