$ErrorActionPreference = "Stop"

Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "                Kokoro Installation for Pearl                 " -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host ""

# Determine install path dynamically (works for any user)
$installBase = [System.Environment]::GetFolderPath("ApplicationData")
$kokoroPath = Join-Path $installBase "Pearl\Kokoro-FastAPI"

Write-Host "Install location:" -ForegroundColor Gray
Write-Host $kokoroPath -ForegroundColor White
Write-Host ""

Write-Host "Press Enter to begin installation..." -ForegroundColor Cyan
Read-Host

# Create directory if it doesn't exist
if (-not (Test-Path $kokoroPath)) {
    Write-Host "Creating install directory..." -ForegroundColor Green
    New-Item -Path $kokoroPath -ItemType Directory -Force | Out-Null
}

Set-Location $kokoroPath

# Check for Git and install if not present
Write-Host "Checking for Git..." -ForegroundColor Gray

$gitAvailable = Get-Command git -ErrorAction SilentlyContinue

if (-not $gitAvailable) {
    Write-Host "Git not found - Git is a requirement to install Kokoro from GitHub." -ForegroundColor Yellow
    Read-Host "Press Enter to install Git for Windows"
    
    $gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/Git-2.47.1-64-bit.exe"
    $gitInstallerPath = "$env:TEMP\GitInstaller.exe"

    try {
        Write-Host "Downloading Git installer..." -ForegroundColor Cyan
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $gitInstallerUrl -OutFile $gitInstallerPath -UseBasicParsing

        Write-Host "Installing Git (you may need admin rights)..." -ForegroundColor Cyan
        Start-Process -FilePath $gitInstallerPath -ArgumentList "/VERYSILENT", "/NORESTART", "/SUPPRESSMSGBOXES", "/CLOSEAPPLICATIONS" -Wait -NoNewWindow

        Remove-Item $gitInstallerPath -Force -ErrorAction SilentlyContinue

        Write-Host "Git installed successfully!" -ForegroundColor Green
        
        # Refresh PATH so current session can see git
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
    }
    catch {
        Write-Host "Failed to install Git automatically." -ForegroundColor Red
        Write-Host "Please install Git manually from https://git-scm.com/download/win" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "Git found: $(git --version)" -ForegroundColor Green
}

# Clone repository if not already present
if (-not (Test-Path "Kokoro-FastAPI")) {
    Write-Host "Cloning Kokoro-FastAPI repository..." -ForegroundColor Green
    git clone https://github.com/remsky/Kokoro-FastAPI.git
} else {
    Write-Host "Kokoro-FastAPI folder already exists. Skipping clone." -ForegroundColor Yellow
}

# Enter the CPU docker folder
Set-Location "Kokoro-FastAPI\docker\cpu"

Write-Host "Building and starting Kokoro..." -ForegroundColor Green
docker compose build
docker compose up -d --build --force-recreate --remove-orphans

# Set containers to restart automatically
Write-Host "Setting containers to restart unless stopped..." -ForegroundColor Gray
docker compose ps -q | ForEach-Object {
    docker update --restart=unless-stopped $_
}

Write-Host ""
Write-Host "Kokoro installation completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Install location: $kokoroPath" -ForegroundColor White
Write-Host "Access Kokoro at: http://localhost:8880" -ForegroundColor Cyan
Write-Host ""
Write-Host "Restart Pearl for enhanced TTS to appear in Settings." -ForegroundColor Yellow
Write-Host "Press Enter to close this window..." -ForegroundColor Gray
Read-Host
exit 0