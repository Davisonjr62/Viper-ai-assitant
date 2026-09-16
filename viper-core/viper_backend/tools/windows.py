import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path

class WindowsTools:
    APPS = {"chrome":"chrome.exe","edge":"msedge.exe","discord":"Discord.exe","spotify":"Spotify.exe","notepad":"notepad.exe","calculator":"calc.exe","vscode":"Code.exe"}
    URLS = {"youtube":"https://youtube.com","gmail":"https://gmail.com","google":"https://google.com","shopify":"https://shopify.com"}

    def open_app(self, parameters):
        app = str(parameters.get("app", "")).lower()
        if app not in self.APPS:
            return {"success": False, "message": f"{app} is not an approved application."}
        try:
            subprocess.Popen([self.APPS[app]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            return {"success": True, "message": f"Opened {app}."}
        except Exception as exc:
            return {"success": False, "message": f"Could not open {app}: {exc}"}

    def open_url(self, parameters):
        site = str(parameters.get("site", "")).lower()
        if site not in self.URLS:
            return {"success": False, "message": f"{site} is not an approved website."}
        try:
            webbrowser.open(self.URLS[site])
            return {"success": True, "message": f"Opened {site}."}
        except Exception as exc:
            return {"success": False, "message": f"Could not open {site}: {exc}"}

    def open_folder(self, parameters):
        folder = str(parameters.get("folder", "")).lower()
        paths = {"downloads":Path.home()/"Downloads","documents":Path.home()/"Documents","desktop":Path.home()/"Desktop"}
        if folder not in paths:
            return {"success": False, "message": f"{folder} is not an approved folder."}
        try:
            subprocess.Popen(["explorer.exe", str(paths[folder])])
            return {"success": True, "message": f"Opened {folder}."}
        except Exception as exc:
            return {"success": False, "message": f"Could not open {folder}: {exc}"}

    def take_screenshot(self, parameters):
        try:
            from PIL import ImageGrab
            target = Path.home()/"Pictures"/"Viper Screenshots"
            target.mkdir(parents=True, exist_ok=True)
            path = target/f"viper_{datetime.now():%Y%m%d_%H%M%S}.png"
            ImageGrab.grab().save(path)
            return {"success": True, "message": f"Screenshot saved to {path}."}
        except Exception as exc:
            return {"success": False, "message": f"Screenshot failed: {exc}"}
