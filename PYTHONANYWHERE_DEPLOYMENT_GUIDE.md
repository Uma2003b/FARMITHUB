# PythonAnywhere Deployment Guide for AgriConnectHub

## Quick Setup Steps

### 1. SSH into PythonAnywhere
```bash
ssh RuralITHUB@ssh.pythonanywhere.com
```

### 2. Navigate to Web App Directory
```bash
cd /home/RuralITHUB/FARMITHUB
```

### 3. Pull Latest Changes from GitHub
```bash
git pull origin main
```

### 4. Reload Web App
```bash
touch /var/www/uma2003b_pythonanywhere_com_wsgi.py
```

---

## Complete Configuration (If Starting Fresh)

### Step 1: Clone Repository
```bash
cd /home/RuralITHUB
git clone https://github.com/Uma2003b/FARMITHUB.git
cd FARMITHUB
```

### Step 2: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 agriconnect
pip install -r requirements.txt
```

### Step 3: Configure WSGI File
Edit `/var/www/RuralITHUB_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

path = '/home/RuralITHUB/FARMITHUB'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

from application import application
```

### Step 4: Update Web App Settings in PythonAnywhere Dashboard
1. Go to **Web** tab
2. Select **agriconnectdashboard-RuralITHUB.pythonanywhere.com**
3. Set **Source code** to: `/home/RuralITHUB/FARMITHUB`
4. Set **Working directory** to: `/home/RuralITHUB/FARMITHUB`
5. Set **WSGI configuration file** to: `/var/www/RuralITHUB_pythonanywhere_com_wsgi.py`
6. Set **Virtualenv** to: `/home/RuralITHUB/.virtualenvs/agriconnect`

### Step 5: Reload Web App
Click **Reload** button in PythonAnywhere Web tab

---

## Automated Deployment Script

Create `/home/RuralITHUB/deploy.sh`:

```bash
#!/bin/bash
cd /home/RuralITHUB/FARMITHUB
git fetch origin
git reset --hard origin/main
touch /var/www/RuralITHUB_pythonanywhere_com_wsgi.py
echo "Deployment complete at $(date)"
```

Make executable:
```bash
chmod +x /home/RuralITHUB/deploy.sh
```

Run deployment:
```bash
/home/RuralITHUB/deploy.sh
```

---

## Troubleshooting

### Changes Not Appearing
1. Verify git pull worked: `git log --oneline -5`
2. Check file timestamps: `ls -la templates/main.html`
3. Reload web app: `touch /var/www/RuralITHUB_pythonanywhere_com_wsgi.py`
4. Check error log: `/var/log/RuralITHUB_pythonanywhere_com.error.log`

### Git Authentication Issues
If git pull fails, set up SSH key:
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub
```
Add public key to GitHub account settings

### Module Import Errors
Verify virtualenv is activated:
```bash
source /home/RuralITHUB/.virtualenvs/agriconnect/bin/activate
pip list
```

---

## Key Files to Monitor

- **Application**: `/home/RuralITHUB/FARMITHUB/application.py`
- **Templates**: `/home/RuralITHUB/FARMITHUB/templates/`
- **WSGI Config**: `/var/www/RuralITHUB_pythonanywhere_com_wsgi.py`
- **Error Log**: `/var/log/RuralITHUB_pythonanywhere_com.error.log`
- **Access Log**: `/var/log/RuralITHUB_pythonanywhere_com.access.log`

---

## Deployment Checklist

- [ ] Repository cloned to `/home/RuralITHUB/FARMITHUB`
- [ ] Virtual environment created and activated
- [ ] `requirements.txt` installed
- [ ] WSGI file configured correctly
- [ ] Web app source code path set correctly
- [ ] Web app reloaded
- [ ] Changes visible at `agriconnectdashboard-RuralITHUB.pythonanywhere.com`
