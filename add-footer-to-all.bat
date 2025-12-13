@echo off
echo Adding shared footer script to all HTML files...

cd /d "c:\Users\umaga\Downloads\Desktop\NEW PROJECTS\AGRICONNECT-HUB-DASHBOARD\templates"

for %%f in (*.html) do (
    echo Processing %%f...
    
    REM Check if file already has shared-footer.js
    findstr /c:"shared-footer.js" "%%f" >nul
    if errorlevel 1 (
        REM Add shared-footer.js before closing body tag
        powershell -Command "(Get-Content '%%f') -replace '</body>', '  <script src=\"shared-footer.js\"></script>^</body>' | Set-Content '%%f'"
        echo Added footer script to %%f
    ) else (
        echo %%f already has footer script
    )
)

echo Done! Footer script added to all HTML files.
pause