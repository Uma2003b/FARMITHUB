# PowerShell script to remove old footers from all HTML files
$projectDir = "c:\Users\umaga\Downloads\Desktop\NEW PROJECTS\AGRICONNECT-HUB-DASHBOARD"
$htmlFiles = Get-ChildItem -Path $projectDir -Filter "*.html" -Recurse

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    
    # Remove old footer HTML (between <footer class="site-footer"> and </footer>)
    $content = $content -replace '(?s)<footer class="site-footer">.*?</footer>', ''
    
    # Remove any standalone footer.site-footer CSS
    $content = $content -replace '(?s)footer\.site-footer\s*\{[^}]*\}', ''
    
    Set-Content -Path $file.FullName -Value $content -NoNewline
    Write-Host "Removed old footer from: $($file.Name)"
}

Write-Host "Old footer removal completed!"