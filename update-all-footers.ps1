$templatesPath = "c:\Users\umaga\Downloads\Desktop\NEW PROJECTS\AGRICONNECT-HUB-DASHBOARD\templates"
$htmlFiles = Get-ChildItem -Path $templatesPath -Filter "*.html"

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Check if file already has shared-footer.js
    if ($content -notmatch "shared-footer\.js") {
        # Add shared-footer.js before closing body tag
        $content = $content -replace "</body>", "  <script src=`"shared-footer.js`"></script>`r`n</body>"
        Set-Content -Path $file.FullName -Value $content
        Write-Host "Added footer script to $($file.Name)"
    } else {
        Write-Host "$($file.Name) already has footer script"
    }
}

Write-Host "Done! All HTML files updated."