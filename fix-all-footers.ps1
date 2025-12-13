$templatesPath = "c:\Users\umaga\Downloads\Desktop\NEW PROJECTS\AGRICONNECT-HUB-DASHBOARD\templates"
$htmlFiles = Get-ChildItem -Path $templatesPath -Filter "*.html"

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Remove old footer HTML patterns
    $content = $content -replace '<style>\s*\.site-footer.*?</style>\s*<footer.*?</footer>', '<!-- Shared Footer will be loaded by JavaScript -->'
    $content = $content -replace '<footer class="site-footer">.*?</footer>', '<!-- Shared Footer will be loaded by JavaScript -->'
    
    # Ensure shared-footer.js is present before closing body tag
    if ($content -notmatch "shared-footer\.js") {
        $content = $content -replace "</body>", "  <script src=`"shared-footer.js`"></script>`r`n</body>"
    }
    
    Set-Content -Path $file.FullName -Value $content
    Write-Host "Fixed footer in $($file.Name)"
}

Write-Host "Done! All footers fixed."