$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not $env:ELEVENLABS_API_KEY) {
  Write-Host 'Set your ElevenLabs API key first:' -ForegroundColor Yellow
  Write-Host '$env:ELEVENLABS_API_KEY="your-key"'
  exit 1
}
py -3.13 -m pip install -r .\requirements.txt
$env:PYTHONPATH = "$PSScriptRoot\viper_backend"
py -3.13 .\viper_backend\main.py
