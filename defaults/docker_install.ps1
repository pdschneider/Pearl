$ErrorActionPreference = "Stop"
Write-Host ""
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "          Docker Desktop Installation for Pearl               " -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is already installed and working
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "Docker is already installed." -ForegroundColor Green
    Write-Host ""
    Read-Host "Press Enter to exit..."
    exit 0
}

Write-Host "This installer is for Windows (Docker Desktop with WSL 2)." -ForegroundColor Yellow
Write-Host ""
Write-Host "The installer is ~600MB and will be downloaded automatically." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to begin installation"

# Download the latest Docker Desktop installer
$installerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
$installerPath = "$env:TEMP\DockerDesktopInstaller.exe"

Write-Host "Downloading Docker Desktop installer..." -ForegroundColor Green
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing

Write-Host ""
Write-Host "Docker Desktop is provided by Docker, Inc. under their Subscription Service Agreement." -ForegroundColor Yellow
Write-Host "By proceeding with installation, you agree to Docker's terms." -ForegroundColor Yellow
Write-Host ""
Write-Host "Full license: https://www.docker.com/legal/docker-subscription-service-agreement" -ForegroundColor Cyan
Write-Host "Docker Desktop licensing overview: https://docs.docker.com/subscription/desktop-license/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Docker also requires about 4GB of disk space." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter if you accept Docker's terms and want to continue (you may need admin rights)"
Write-Host ""

# Run the installer silently with license acceptance
Write-Host "Installing Docker (this may take several minutes)..." -ForegroundColor Green
Write-Host ""
Start-Process -FilePath $installerPath -ArgumentList "install", "--quiet", "--accept-license" -Wait -NoNewWindow

# Clean up installer
Remove-Item $installerPath -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Updating WSL..." -ForegroundColor Green
Write-Host ""
wsl.exe --update

# Docker Path
$dockerExe = "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Start Docker Desktop
Write-Host ""
Write-Host "Docker Desktop will now open in a new window to start its service." -ForegroundColor Green
Write-Host "There is no need to sign in - simply close the Window or click 'skip'." -ForegroundColor Green
Write-Host ""
if (Test-Path $dockerExe) {
    Start-Process $dockerExe -WindowStyle Minimized
    Write-Host "Docker Desktop has been started." -ForegroundColor Green
} else {
    Write-Host "Warning: Could not find Docker Desktop.exe" -ForegroundColor Yellow
}

# Settings FIle Path
$settingsPath = "$env:APPDATA\Docker\settings-store.json"

# Enable AutoStart (and disable opening the GUI on startup)
Start-Sleep -Seconds 3
if (Test-Path $settingsPath) {
    try {
        $settings = Get-Content $settingsPath -Raw | ConvertFrom-Json

        $settings.AutoStart = $true
        if ($settings.PSObject.Properties.Name -contains 'OpenUIOnStartupDisabled') {
            $settings.OpenUIOnStartupDisabled = $true
        } else {
            $settings | Add-Member -NotePropertyName 'OpenUIOnStartupDisabled' -NotePropertyValue $true
        }

        $settings | ConvertTo-Json -Depth 20 | Set-Content $settingsPath -Force

        Write-Host "AutoStart enabled successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "Failed to update settings-store.json: $($_.Exception.Message)" -ForegroundColor Yellow
    }
} else {
    Write-Host "settings-store.json not found yet." -ForegroundColor Yellow
}

# Wait a moment and check if Docker is now available
Write-Host ""
Write-Host "Verifying Install was Successful..." -ForegroundColor Yellow

$maxWait = 30
$timer = [System.Diagnostics.Stopwatch]::StartNew()
$dockerReady = $false

while ($timer.Elapsed.TotalSeconds -lt $maxWait) {
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        try {
            docker version --format "{{.Server.Version}}" | Out-Null
            $dockerReady = $true
            break
        }
        catch {
            Start-Sleep -Seconds 5
        }
    }
    Start-Sleep -Seconds 5
}

if ($dockerReady) {
    Write-Host "Docker Desktop is now installed and the engine is ready!" -ForegroundColor Green
    Write-Host "Docker version: $(docker --version)" -ForegroundColor Green
} else {
    Write-Host "Docker installed, but the engine is still starting up." -ForegroundColor Yellow
    Write-Host "Please wait a bit longer or restart your PC for Docker to take effect." -ForegroundColor Yellow
}

Write-Host 'Press Enter to close this window and return to Pearl...'
Read-Host
exit 0