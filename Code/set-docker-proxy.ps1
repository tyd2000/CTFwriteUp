# set-docker-proxy.ps1
Write-Host "Configuring Docker Desktop to use proxy http://127.0.0.1:7890 ..."

# Stop Docker Desktop
Write-Host "Stopping Docker Desktop..."
Stop-Process -Name "Docker Desktop" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

# Path to config file
$configPath = "$env:APPDATA\Docker\settings.json"

# Create proxy config object
$proxyConfig = [PSCustomObject]@{
    proxies = @{
        http    = "http://127.0.0.1:7890"
        https   = "http://127.0.0.1:7890"
        noProxy = "localhost,127.0.0.1,.local"
    }
}

# Save to file
$proxyConfig | ConvertTo-Json -Depth 10 | Set-Content -Path $configPath -Encoding UTF8

Write-Host "Config saved to: $configPath"
Write-Host "Starting Docker Desktop..."

# Use full path to avoid "file not found"
$dockerPath = "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe"
if (Test-Path $dockerPath) {
    Start-Process -FilePath $dockerPath
} else {
    Write-Host "Warning: Docker Desktop.exe not found at expected path." -ForegroundColor Yellow
    Write-Host "Please start Docker Desktop manually from Start Menu." -ForegroundColor Yellow
}

Write-Host "Done! Wait for Docker to start, then run 'docker info' to verify."