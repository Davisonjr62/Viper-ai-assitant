$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
py -3.13 --version
if (-not $env:ELEVENLABS_API_KEY) {
  Write-Host 'Set your ElevenLabs API key first:' -ForegroundColor Yellow
  Write-Host '$env:ELEVENLABS_API_KEY="your-key"'
  exit 1
}
py -3.13 -m pip install -r .\requirements.txt
$env:PYTHONPATH = "$PSScriptRoot\viper_backend"
py -3.13 -c "from tools.windows import WindowsTools; print('Windows tools loaded:', ', '.join(WindowsTools.APPS.Keys))"
Write-Host 'Viper backend preflight passed.' -ForegroundColor Green
