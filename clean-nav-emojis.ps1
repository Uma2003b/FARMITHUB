# PowerShell script to remove emojis from navigation links
$projectDir = "c:\Users\umaga\Downloads\Desktop\NEW PROJECTS\AGRICONNECT-HUB-DASHBOARD"
$htmlFiles = Get-ChildItem -Path $projectDir -Filter "*.html" -Recurse

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    
    # Replace specific navigation patterns
    $content = $content -replace '<a href="/crop_recommendation/">🌱 Crop Recommendation</a>', '<a href="/crop_recommendation/">Crop Recommendation</a>'
    $content = $content -replace '<a href="/crop_yield/">📊 Yield Prediction</a>', '<a href="/crop_yield/">Yield Prediction</a>'
    $content = $content -replace '<a href="disease.html">🔬 Disease Prediction</a>', '<a href="disease.html">Disease Prediction</a>'
    $content = $content -replace '<a href="organic.html">🌿 Organic Farming</a>', '<a href="organic.html">Organic Farming</a>'
    $content = $content -replace '<a href="farmer.html">👥 Farmer Network</a>', '<a href="farmer.html">Farmer Network</a>'
    $content = $content -replace '<a href="weather.html">⛅ Weather Check</a>', '<a href="weather.html">Weather Check</a>'
    $content = $content -replace '<a href="shopkeeper.html">🏪 Shopkeeper Listings</a>', '<a href="shopkeeper.html">Shopkeeper Listings</a>'
    $content = $content -replace '<a href="chat.html">🤖 ChatBot</a>', '<a href="chat.html">ChatBot</a>'
    $content = $content -replace '<a href="plantation.html">🌳 Plantation</a>', '<a href="plantation.html">Plantation</a>'
    $content = $content -replace '<a href="/crop_planning/">📅 Crop Planning</a>', '<a href="/crop_planning/">Crop Planning</a>'
    $content = $content -replace '<a href="./Labour_Alerts/templates/labour.html">⚠ Labour Alerts</a>', '<a href="./Labour_Alerts/templates/labour.html">Labour Alerts</a>'
    $content = $content -replace '<a href="/sugarcane_frp/">🍯 Sugarcane FRP</a>', '<a href="/sugarcane_frp/">Sugarcane FRP</a>'
    $content = $content -replace '<a href="/district_procurement/">📦 District Procurement</a>', '<a href="/district_procurement/">District Procurement</a>'
    
    Set-Content -Path $file.FullName -Value $content -NoNewline
    Write-Host "Cleaned nav emojis in: $($file.Name)"
}

Write-Host "Navigation emoji cleanup completed!"