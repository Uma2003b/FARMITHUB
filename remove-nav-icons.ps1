# PowerShell script to remove emoji icons from navigation across all HTML files
$projectDir = "c:\Users\umaga\Downloads\Desktop\NEW PROJECTS\AGRICONNECT-HUB-DASHBOARD"
$htmlFiles = Get-ChildItem -Path $projectDir -Filter "*.html" -Recurse

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    
    # Remove emojis from navigation links
    $content = $content -replace '🌱 ', ''
    $content = $content -replace '📊 ', ''
    $content = $content -replace '🔬 ', ''
    $content = $content -replace '🌿 ', ''
    $content = $content -replace '👥 ', ''
    $content = $content -replace '⛅ ', ''
    $content = $content -replace '🏪 ', ''
    $content = $content -replace '🤖 ', ''
    $content = $content -replace '🌳 ', ''
    $content = $content -replace '📅 ', ''
    $content = $content -replace '⚠️ ', ''
    $content = $content -replace '⚠ ', ''
    $content = $content -replace '🍯 ', ''
    $content = $content -replace '📦 ', ''
    
    Set-Content -Path $file.FullName -Value $content -NoNewline
    Write-Host "Removed nav icons from: $($file.Name)"
}

Write-Host "Navigation icon removal completed!"