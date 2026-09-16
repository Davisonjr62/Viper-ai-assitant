# Viper Core — ElevenLabs Voice Backend

Backend-first Viper. No Electron, React, or orb yet.

Architecture:

`Microphone -> ElevenLabs Agents -> GPT-5.6 Luna -> Viper client tools -> Windows`

ElevenLabs handles the realtime voice conversation. GPT-5.6 Luna is selected in the ElevenLabs Agent. This Python process registers local client tools that run on the Windows PC.

## Requirements

- Windows 10/11
- Python 3.13 64-bit
- ElevenLabs account/API key
- Viper ElevenLabs Agent configured for GPT-5.6 Luna
- Microphone and speakers

## PowerShell

```powershell
$env:ELEVENLABS_API_KEY="your-key"
$env:VIPER_AGENT_ID="agent_7001m2na03rgfv6teda5dc0pm83d"
.\TEST_VIPER.ps1
.\START_VIPER.ps1
```

Keep the API key private. Do not commit it to GitHub.

## Current local tools

- `open_app`: Chrome, Edge, Discord, Spotify, Notepad, Calculator, VS Code
- `open_url`: YouTube, Gmail, Google, Shopify
- `open_folder`: Downloads, Documents, Desktop
- `take_screenshot`: saves to Pictures/Viper Screenshots

The tool definitions must be created as **Client** tools in the ElevenLabs Agent with the same names and parameters. Enable **Wait for response** for tools where Viper should wait for the Windows result before speaking.

## Next milestone

Run the backend from PowerShell and verify microphone, speech, response audio, and one Windows tool call before adding Hermes or a UI.
