# PowerShell script to remove emoji icons from navigation across all HTML files
$projectDir = "c:\Users\umaga\Downloads\Desktop\NEW PROJECTS\AGRICONNECT-HUB-DASHBOARD"
$htmlFiles = Get-ChildItem -Path $projectDir -Filter "*.html" -Recurse

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    
    # Remove navigation text patterns
    $content = $content -replace 'Crop Recommendation</a>', 'Crop Recommendation</a>'
    $content = $content -replace 'Yield Prediction</a>', 'Yield Prediction</a>'
    $content = $content -replace 'Disease Prediction</a>', 'Disease Prediction</a>'
    $content = $content -replace 'Organic Farming</a>', 'Organic Farming</a>'
    $content = $content -replace 'Farmer Network</a>', 'Farmer Network</a>'
    $content = $content -replace 'Weather Check</a>', 'Weather Check</a>'
    $content = $content -replace 'Shopkeeper Listings</a>', 'Shopkeeper Listings</a>'
    $content = $content -replace 'ChatBot</a>', 'ChatBot</a>'
    $content = $content -replace 'Plantation</a>', 'Plantation</a>'
    $content = $content -replace 'Crop Planning</a>', 'Crop Planning</a>'
    $content = $content -replace 'Labour Alerts</a>', 'Labour Alerts</a>'
    $content = $content -replace 'Sugarcane FRP</a>', 'Sugarcane FRP</a>'
    $content = $content -replace 'District Procurement</a>', 'District Procurement</a>'
    
    # Remove emoji patterns from nav links
    $content = $content -replace '>\s*[^\w<>]*\s*Crop Recommendation', '>Crop Recommendation'
    $content = $content -replace '>\s*[^\w<>]*\s*Yield Prediction', '>Yield Prediction'
    $content = $content -replace '>\s*[^\w<>]*\s*Disease Prediction', '>Disease Prediction'
    $content = $content -replace '>\s*[^\w<>]*\s*Organic Farming', '>Organic Farming'
    $content = $content -replace '>\s*[^\w<>]*\s*Farmer Network', '>Farmer Network'
    $content = $content -replace '>\s*[^\w<>]*\s*Weather Check', '>Weather Check'
    $content = $content -replace '>\s*[^\w<>]*\s*Shopkeeper Listings', '>Shopkeeper Listings'
    $content = $content -replace '>\s*[^\w<>]*\s*ChatBot', '>ChatBot'
    $content = $content -replace '>\s*[^\w<>]*\s*Plantation', '>Plantation'
    $content = $content -replace '>\s*[^\w<>]*\s*Crop Planning', '>Crop Planning'
    $content = $content -replace '>\s*[^\w<>]*\s*Labour Alerts', '>Labour Alerts'
    $content = $content -replace '>\s*[^\w<>]*\s*Sugarcane FRP', '>Sugarcane FRP'
    $content = $content -replace '>\s*[^\w<>]*\s*District Procurement', '>District Procurement'
    
    Set-Content -Path $file.FullName -Value $content -NoNewline
    Write-Host "Cleaned nav in: $($file.Name)"
}

Write-Host "Navigation cleanup completed!"