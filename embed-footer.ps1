# PowerShell script to embed footer JavaScript directly in all HTML files
$templateDir = "c:\Users\umaga\Downloads\Desktop\NEW PROJECTS\AGRICONNECT-HUB-DASHBOARD\templates"
$htmlFiles = Get-ChildItem -Path $templateDir -Filter "*.html"

$footerScript = @"
  <script>
    // Shared Footer Loader
    document.addEventListener('DOMContentLoaded', function() {
      // Create footer if it doesn't exist
      if (!document.querySelector('.site-footer')) {
        const footerHTML = `
          <style>
            .site-footer {
              background: linear-gradient(135deg, #2e7d32, #66bb6a);
              color: #fff;
              margin-top: auto;
              padding: 1.5rem;
              text-align: center;
              font-size: 0.9rem;
            }
            .site-footer a {
              color: #fff;
              text-decoration: none;
            }
            .site-footer a:hover {
              text-decoration: underline;
            }
          </style>
          <footer class="site-footer">
            <p>&copy; 2025 Rural-IT-Hub. All rights reserved. powered by technoble.solutions. Email: <a href="mailto:admin@ruralithub.net">admin@ruralithub.net</a></p>
          </footer>
        `;
        
        // Insert footer before closing body tag
        document.body.insertAdjacentHTML('beforeend', footerHTML);
      }
    });
  </script>
"@

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    
    # Replace external script reference with embedded script
    if ($content -match '<script src="shared-footer\.js"></script>') {
        $content = $content -replace '<script src="shared-footer\.js"></script>', $footerScript
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "Updated: $($file.Name)"
    }
    # Add script if it doesn't exist
    elseif ($content -notmatch 'Shared Footer Loader') {
        $content = $content -replace '</body>', "$footerScript`r`n</body>"
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "Added footer to: $($file.Name)"
    }
}

Write-Host "Footer embedding completed!"