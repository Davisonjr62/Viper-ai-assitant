# ElevenLabs Client Tools for Viper

Create these under **Agent -> Tools -> Add Tool -> Client**. Names are case-sensitive and must match the Python backend.

## open_app
Description: Open an approved Windows application on Mr. David's PC. Use when the user asks to open, launch, start, or bring up an application.

Parameter:
- `app` — string, required
- Allowed values: `chrome`, `edge`, `discord`, `spotify`, `notepad`, `calculator`, `vscode`

Enable **Wait for response**.

## open_url
Description: Open an approved website in the user's default browser.

Parameter:
- `site` — string, required
- Allowed values: `youtube`, `gmail`, `google`, `shopify`

Enable **Wait for response**.

## open_folder
Description: Open an approved Windows user folder.

Parameter:
- `folder` — string, required
- Allowed values: `downloads`, `documents`, `desktop`

Enable **Wait for response**.

## take_screenshot
Description: Take a screenshot of the Windows desktop and save it to Viper's screenshot folder. Use when the user explicitly asks for a screenshot.

No parameters.

Enable **Wait for response**.

## Important

Do not add arbitrary shell execution or unrestricted PowerShell as an ElevenLabs client tool at this stage. Keep the Windows tool surface allowlisted until the basic voice-to-action loop is proven.
