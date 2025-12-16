# PowerShell script to add language manager to all HTML files
$templateDir = "templates"
$htmlFiles = Get-ChildItem -Path $templateDir -Filter "*.html" | Where-Object { $_.Name -ne "shared-footer.html" }

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Check if language-manager.js is already included
    if ($content -notmatch "language-manager\.js") {
        # Add language manager script before </head>
        $content = $content -replace "</head>", "  <script src=`"language-manager.js`"></script>`n</head>"
        
        # Write back to file
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "Added language manager to: $($file.Name)"
    } else {
        Write-Host "Language manager already exists in: $($file.Name)"
    }
}

Write-Host "Language manager setup complete!"