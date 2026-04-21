import base64
import json
import threading
import time
import sys
import tkinter as tk
from tkinter import simpledialog
from io import BytesIO

import pyautogui
import requests
from PIL import Image
from pynput import keyboard

OLLAMA_URL = "http://5.189.173.84:11434"
MODEL = "gemma4:latest"

triggered = threading.Event()


def screenshot_b64():
    img = pyautogui.screenshot()
    img = img.resize((800, 450), Image.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def ask_ollama(image_b64, command):
    prompt = f"""You are a PC automation agent. The user wants: "{command}"

Look at the screenshot and respond with a JSON array of actions.
Each action must be one of:
- {{"type": "click", "x": 100, "y": 200}}
- {{"type": "type", "text": "hello world"}}
- {{"type": "hotkey", "keys": ["ctrl", "c"]}}
- {{"type": "scroll", "x": 100, "y": 200, "amount": 3}}
- {{"type": "wait", "seconds": 1}}
- {{"type": "done", "message": "task complete"}}

Respond ONLY with a valid JSON array. No explanation. No markdown.
Screen is scaled to 800x450.
"""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "images": [image_b64],
        "stream": False,
    }
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=300)
    r.raise_for_status()
    return r.json()["response"]


def execute_actions(actions_str):
    try:
        raw = actions_str.strip()
        if "```" in raw:
            parts = raw.split("```")
            raw = parts[1] if len(parts) > 1 else parts[0]
            if raw.startswith("json"):
                raw = raw[4:]
        actions = json.loads(raw.strip())
    except Exception:
        print(f"[!] Could not parse: {actions_str[:300]}")
        return

    real_w, real_h = pyautogui.size()
    sx = real_w / 800
    sy = real_h / 450

    for action in actions:
        t = action.get("type")
        if t == "click":
            x, y = int(action["x"] * sx), int(action["y"] * sy)
            print(f"  -> click ({x}, {y})")
            pyautogui.click(x, y)
        elif t == "type":
            print(f"  -> type: {action['text'][:60]}")
            pyautogui.write(action["text"], interval=0.04)
        elif t == "hotkey":
            keys = [k.lstrip("+") for k in action["keys"]]
            print(f"  -> hotkey: {keys}")
            pyautogui.hotkey(*keys)
        elif t == "scroll":
            x, y = int(action["x"] * sx), int(action["y"] * sy)
            pyautogui.scroll(action.get("amount", 3), x=x, y=y)
        elif t == "enter":
            pyautogui.press("enter")
        elif t == "wait":
            time.sleep(action.get("seconds", 1))
        elif t == "done":
            print(f"  -> {action.get('message', 'done')}")
        time.sleep(0.3)


def hotkey_listener():
    def on_press(key):
        if key == keyboard.Key.f9:
            triggered.set()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def ask_command():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    command = simpledialog.askstring(
        "Lizzarss",
        "What do you want me to do?\n\nTip: start with 'look:' to include a screenshot (slower)",
        parent=root
    )
    root.destroy()
    return command.strip() if command else ""


def ask_ollama_text(command):
    prompt = f"""You are a PC automation agent on Windows. The user wants: "{command}"

Respond with a JSON array of actions to perform. Each action:
- {{"type": "click", "x": 100, "y": 200}}
- {{"type": "type", "text": "hello"}}
- {{"type": "hotkey", "keys": ["ctrl", "c"]}}
- {{"type": "wait", "seconds": 1}}
- {{"type": "done", "message": "complete"}}

IMPORTANT rules:
1. To open an app: use {{"type":"hotkey","keys":["win","r"]}}, then type app name, then {{"type":"enter"}}, then {{"type":"wait","seconds":2}}
2. Only type text AFTER the app is open and waiting
3. Use "notepad" not "notepad.exe" in run dialog
Respond ONLY with a valid JSON array. No markdown. No extra text.
"""
    payload = {"model": "llama3.1:latest", "prompt": prompt, "stream": False, "keep_alive": -1}
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["response"]


def run():
    print("=== Lizzarss Agent ===")
    print(f"Hotkey: F9")
    print(f"Brain: {MODEL} @ {OLLAMA_URL}")
    print("Press F9 to activate, Ctrl+C to quit\n")

    t = threading.Thread(target=hotkey_listener, daemon=True)
    t.start()

    while True:
        triggered.wait()
        triggered.clear()
        try:
            command = ask_command()
            if not command:
                continue
            if command.lower().startswith("look:"):
                command = command[5:].strip()
                print("[Lizzarss] Taking screenshot...")
                img_b64 = screenshot_b64()
                print("[Lizzarss] Thinking with vision (30-60s)...")
                response = ask_ollama(img_b64, command)
            else:
                print("[Lizzarss] Thinking (fast mode)...")
                response = ask_ollama_text(command)
            print(f"[Lizzarss] Got response, executing...\n{response[:200]}\n")
            execute_actions(response)
            print("[Lizzarss] Done. Press F9 for next command.\n")
        except KeyboardInterrupt:
            print("\n[Lizzarss] Stopped.")
            sys.exit(0)
        except Exception as e:
            print(f"[!] Error: {e}\n")


if __name__ == "__main__":
    run()
