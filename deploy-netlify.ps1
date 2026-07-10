# Simple Netlify deploy via API
$token = "nfp_HGHovugyYo1CcLdyg8F9q9ZdFvw5Qz8q0f00"

# Create a site
$body = @{name="act-project-web"; custom_domain=$null} | ConvertTo-Json
$site = Invoke-RestMethod -Uri "https://api.netlify.com/api/v1/sites" -Method Post -Headers @{Authorization="Bearer $token"} -ContentType "application/json" -Body $body

Write-Host "Site created: $($site.ssl_url)"

# Upload the tar file as deploy
$fileBytes = [System.IO.File]::ReadAllBytes("$PSScriptRoot\website-deploy.tar")
$deploy = Invoke-RestMethod -Uri "https://api.netlify.com/api/v1/sites/$($site.id)/deploys" -Method Post -Headers @{Authorization="Bearer $token"} -ContentType "application/octet-stream" -Body $fileBytes

Write-Host "Deployed! URL: $($deploy.ssl_url)"
Write-Host "Admin: $($deploy.admin_url)"