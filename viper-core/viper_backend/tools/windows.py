import ctypes
import os
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path

try:
    import pyautogui
except ImportError:
    pyautogui = None

try:
    import pyperclip
except ImportError:
    pyperclip = None


class WindowsTools:
    APPS = {
        "chrome": "chrome.exe", "edge": "msedge.exe", "discord": "Discord.exe",
        "spotify": "Spotify.exe", "notepad": "notepad.exe", "calculator": "calc.exe",
        "vscode": "Code.exe",
    }
    URLS = {"youtube": "https://youtube.com", "gmail": "https://gmail.com", "google": "https://google.com", "shopify": "https://shopify.com"}

    def _result(self, success, message):
        return {"success": success, "message": message}

    def open_app(self, parameters):
        app = str(parameters.get("app", "")).lower().strip()
        if app not in self.APPS:
            return self._result(False, f"{app} is not an approved application.")
        try:
            subprocess.Popen([self.APPS[app]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            return self._result(True, f"Opened {app}.")
        except Exception as exc:
            return self._result(False, f"Could not open {app}: {exc}")

    def open_url(self, parameters):
        value = str(parameters.get("url", parameters.get("site", ""))).strip()
        aliases = {**self.URLS, "https://youtube.com": "https://youtube.com", "https://gmail.com": "https://gmail.com", "https://google.com": "https://google.com", "https://shopify.com": "https://shopify.com"}
        url = aliases.get(value.lower())
        if not url and value.startswith("https://") and value.split("/")[2] in {"youtube.com", "www.youtube.com", "gmail.com", "www.gmail.com", "google.com", "www.google.com", "shopify.com", "www.shopify.com"}:
            url = value
        if not url:
            return self._result(False, "That website is not approved.")
        try:
            webbrowser.open(url)
            return self._result(True, f"Opened {url}.")
        except Exception as exc:
            return self._result(False, f"Could not open the website: {exc}")

    def open_folder(self, parameters):
        folder = str(parameters.get("folder", "")).lower().strip()
        paths = {"downloads": Path.home() / "Downloads", "documents": Path.home() / "Documents", "desktop": Path.home() / "Desktop"}
        if folder not in paths:
            return self._result(False, f"{folder} is not an approved folder.")
        try:
            subprocess.Popen(["explorer.exe", str(paths[folder])])
            return self._result(True, f"Opened {folder}.")
        except Exception as exc:
            return self._result(False, f"Could not open {folder}: {exc}")

    def take_screenshot(self, parameters):
        try:
            from PIL import ImageGrab
            target = Path.home() / "Pictures" / "Viper Screenshots"
            target.mkdir(parents=True, exist_ok=True)
            path = target / f"viper_{datetime.now():%Y%m%d_%H%M%S}.png"
            ImageGrab.grab().save(path)
            return self._result(True, f"Screenshot saved to {path}.")
        except Exception as exc:
            return self._result(False, f"Screenshot failed: {exc}")

    def lock_pc(self, parameters):
        try:
            ctypes.windll.user32.LockWorkStation()
            return self._result(True, "Locked the PC.")
        except Exception as exc:
            return self._result(False, f"Could not lock the PC: {exc}")

    def play_media(self, parameters):
        query = str(parameters.get("query", "")).strip()
        if not query:
            return self._result(False, "No media query was provided.")
        try:
            webbrowser.open("https://www.youtube.com/results?search_query=" + __import__("urllib.parse").parse.quote(query))
            return self._result(True, f"Opened YouTube results for {query}.")
        except Exception as exc:
            return self._result(False, f"Could not open media: {exc}")

    def open_settings(self, parameters):
        try:
            subprocess.Popen(["start", "ms-settings:"], shell=True)
            return self._result(True, "Opened Windows Settings.")
        except Exception as exc:
            return self._result(False, f"Could not open Settings: {exc}")

    def control_volume(self, parameters):
        if pyautogui is None:
            return self._result(False, "Volume control dependency is unavailable.")
        action = str(parameters.get("action", "")).lower().strip()
        try:
            if action == "increase": pyautogui.press("volumeup")
            elif action == "decrease": pyautogui.press("volumedown")
            elif action == "mute": pyautogui.press("volumemute")
            elif action == "unmute": pyautogui.press("volumemute")
            elif action == "set":
                level = max(0, min(100, int(float(parameters.get("level", 50)))))
                for _ in range(50): pyautogui.press("volumedown")
                for _ in range(round(level / 2)): pyautogui.press("volumeup")
            else: return self._result(False, "Unknown volume action.")
            return self._result(True, f"Volume action completed: {action}.")
        except Exception as exc:
            return self._result(False, f"Volume control failed: {exc}")

    def clipboard(self, parameters):
        if pyperclip is None:
            return self._result(False, "Clipboard dependency is unavailable.")
        action = str(parameters.get("action", "")).lower().strip()
        try:
            if action == "read": return self._result(True, pyperclip.paste())
            if action == "write": pyperclip.copy(str(parameters.get("text", ""))); return self._result(True, "Clipboard updated.")
            return self._result(False, "Clipboard action must be read or write.")
        except Exception as exc:
            return self._result(False, f"Clipboard operation failed: {exc}")

    def type_text(self, parameters):
        if pyautogui is None: return self._result(False, "Keyboard control dependency is unavailable.")
        try:
            pyautogui.write(str(parameters.get("text", "")), interval=0.002)
            return self._result(True, "Text typed.")
        except Exception as exc: return self._result(False, f"Typing failed: {exc}")

    def press_key(self, parameters):
        if pyautogui is None: return self._result(False, "Keyboard control dependency is unavailable.")
        try:
            raw = str(parameters.get("key", "")).strip()
            parts = [p.strip().lower() for p in raw.replace(" ", "").split("+")]
            if len(parts) > 1: pyautogui.hotkey(*parts)
            else: pyautogui.press(parts[0])
            return self._result(True, f"Pressed {raw}.")
        except Exception as exc: return self._result(False, f"Key press failed: {exc}")

    def mouse_click(self, parameters):
        if pyautogui is None: return self._result(False, "Mouse control dependency is unavailable.")
        try: pyautogui.click(int(parameters["x"]), int(parameters["y"])); return self._result(True, "Clicked the requested location.")
        except Exception as exc: return self._result(False, f"Click failed: {exc}")

    def mouse_move(self, parameters):
        if pyautogui is None: return self._result(False, "Mouse control dependency is unavailable.")
        try: pyautogui.moveTo(int(parameters["x"]), int(parameters["y"]), duration=0.1); return self._result(True, "Moved the cursor.")
        except Exception as exc: return self._result(False, f"Mouse move failed: {exc}")

    def mouse_scroll(self, parameters):
        if pyautogui is None: return self._result(False, "Mouse control dependency is unavailable.")
        try: pyautogui.scroll(int(parameters["amount"])); return self._result(True, "Scrolled.")
        except Exception as exc: return self._result(False, f"Scroll failed: {exc}")

    def mouse_drag(self, parameters):
        if pyautogui is None: return self._result(False, "Mouse control dependency is unavailable.")
        try:
            pyautogui.moveTo(int(parameters["start_x"]), int(parameters["start_y"]), duration=0.1)
            pyautogui.dragTo(int(parameters["end_x"]), int(parameters["end_y"]), duration=0.3, button="left")
            return self._result(True, "Dragged successfully.")
        except Exception as exc: return self._result(False, f"Drag failed: {exc}")

    def get_screen_info(self, parameters):
        if pyautogui is None: return self._result(False, "Screen information dependency is unavailable.")
        try:
            size = pyautogui.size()
            return self._result(True, {"width": size.width, "height": size.height})
        except Exception as exc: return self._result(False, f"Could not get screen info: {exc}")

    def get_active_window(self, parameters):
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
            return self._result(True, {"title": buf.value, "hwnd": hwnd})
        except Exception as exc: return self._result(False, f"Could not get active window: {exc}")

    def get_screen_image(self, parameters):
        return self.take_screenshot(parameters)

    def close_app(self, parameters):
        app = str(parameters.get("app", "")).lower().strip()
        exe = self.APPS.get(app)
        if not exe: return self._result(False, f"{app} is not an approved application.")
        try:
            subprocess.run(["taskkill", "/IM", exe, "/T", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            return self._result(True, f"Closed {app}.")
        except Exception as exc: return self._result(False, f"Could not close {app}: {exc}")

    def open_task_manager(self, parameters):
        try: subprocess.Popen(["taskmgr.exe"]); return self._result(True, "Opened Task Manager.")
        except Exception as exc: return self._result(False, f"Could not open Task Manager: {exc}")

    def restart_app(self, parameters):
        result = self.close_app(parameters)
        if not result["success"]: return result
        return self.open_app(parameters)

    def minimize_all_windows(self, parameters):
        if pyautogui is None: return self._result(False, "Keyboard control dependency is unavailable.")
        try: pyautogui.hotkey("win", "d"); return self._result(True, "Minimized all windows.")
        except Exception as exc: return self._result(False, f"Could not minimize windows: {exc}")

    def show_desktop(self, parameters):
        return self.minimize_all_windows(parameters)

    def shutdown_pc(self, parameters):
        try:
            subprocess.Popen(["shutdown", "/s", "/t", "5"], creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            return self._result(True, "Windows shutdown was scheduled in 5 seconds.")
        except Exception as exc: return self._result(False, f"Could not schedule shutdown: {exc}")
