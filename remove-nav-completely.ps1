# PowerShell script to remove entire navigation section from all HTML files
$projectDir = "c:\Users\umaga\Downloads\Desktop\NEW PROJECTS\AGRICONNECT-HUB-DASHBOARD"
$htmlFiles = Get-ChildItem -Path $projectDir -Filter "*.html" -Recurse

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    
    # Remove entire nav section
    $content = $content -replace '(?s)<nav>.*?</nav>', ''
    
    Set-Content -Path $file.FullName -Value $content -NoNewline
    Write-Host "Removed nav from: $($file.Name)"
}

Write-Host "Navigation removal completed!"