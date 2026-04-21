# ============================================================
# LIZZARSS - Local AI PC Automation Agent
# Press F9, tell it what to do, watch it happen
# ============================================================

# These are the libraries we need — install them with:
# pip install pyautogui pillow requests pynput
import base64        # converts screenshots to text so we can send them to AI
import json          # parses the AI's response (it sends back JSON)
import threading     # lets the hotkey listener run in the background
import time          # used for waiting between actions
import sys           # used to exit the program cleanly
import tkinter       # built into Python — used for the popup dialog
from tkinter import simpledialog  # the small input box that appears when you press F9
from io import BytesIO            # helps us handle image data in memory

import pyautogui     # controls your mouse and keyboard
import requests      # sends requests to the AI (Groq or Ollama)
from PIL import Image            # resizes screenshots before sending to AI
from pynput import keyboard      # listens for the F9 hotkey in the background


# ============================================================
# CONFIGURATION — change these to match your setup
# ============================================================

# --- OPTION 1: GROQ (recommended for low-end PCs) ---
# Groq is a free cloud AI — fast, no GPU needed, works on any PC
# Get your free API key at: console.groq.com
GROQ_API_KEY = ""  # paste your Groq key here between the quotes
GROQ_MODEL = "llama-3.3-70b-versatile"  # the AI model to use on Groq

# --- OPTION 2: OLLAMA (for people who want everything local) ---
# Ollama runs AI on your own machine — needs ~5GB free space + Ollama installed
# Download Ollama at: ollama.com/download, then run: ollama pull llama3.1
OLLAMA_URL = "http://localhost:11434"  # where Ollama runs on your PC
OLLAMA_MODEL = "llama3.1"             # the model to use with Ollama

# This automatically picks Groq if you filled in the API key, otherwise uses Ollama
USE_GROQ = bool(GROQ_API_KEY)

# ============================================================

# This is a signal — when F9 is pressed, it "fires" and wakes up the main loop
triggered = threading.Event()


def screenshot_b64():
    # Takes a screenshot of your entire screen
    img = pyautogui.screenshot()
    # Resize it to a smaller size so it's faster to send to the AI
    img = img.resize((800, 450), Image.LANCZOS)
    # Save it into memory (not to disk) as a PNG file
    buf = BytesIO()
    img.save(buf, format="PNG")
    # Convert it to base64 text so we can send it inside a JSON request
    return base64.b64encode(buf.getvalue()).decode()


def build_prompt(command):
    # This is the instruction we send to the AI every time
    # It tells the AI exactly what format to respond in
    return f"""You are a PC automation agent on Windows. The user wants: "{command}"

Respond with a JSON array of actions to perform. Each action must be one of these types:
- {{"type": "click", "x": 100, "y": 200}}        <- clicks at position x,y on screen
- {{"type": "type", "text": "hello"}}              <- types text using keyboard
- {{"type": "hotkey", "keys": ["ctrl", "c"]}}      <- presses keyboard shortcuts
- {{"type": "enter"}}                              <- presses the Enter key
- {{"type": "wait", "seconds": 1}}                 <- pauses before next action
- {{"type": "done", "message": "complete"}}        <- signals the task is finished

IMPORTANT rules you must follow:
1. To open any app: first use {{"type":"hotkey","keys":["win","r"]}} to open the Run dialog,
   then type the app name, then {{"type":"enter"}}, then {{"type":"wait","seconds":2}} to let it load
2. Only type text AFTER the app is already open and ready
3. Use "notepad" not "notepad.exe" in the run dialog

Respond ONLY with a valid JSON array. No markdown. No explanation. Just the JSON.
"""


def ask_groq(command):
    # Sends the command to Groq's cloud API and gets back a list of actions
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",  # your API key for authentication
        "Content-Type": "application/json"           # tells Groq we're sending JSON
    }
    payload = {
        "model": GROQ_MODEL,  # which AI model to use
        "messages": [{"role": "user", "content": build_prompt(command)}],  # the instruction
        "temperature": 0.1    # low temperature = more predictable, consistent responses
    }
    # Send the request and wait up to 30 seconds for a response
    r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=30)
    r.raise_for_status()  # crash loudly if something went wrong
    # Pull out just the text response from the JSON Groq sends back
    return r.json()["choices"][0]["message"]["content"]


def ask_ollama_text(command):
    # Sends the command to Ollama running locally on this machine
    payload = {
        "model": OLLAMA_MODEL,          # which local model to use
        "prompt": build_prompt(command), # the instruction
        "stream": False,                 # wait for full response, don't stream it
        "keep_alive": -1                 # keep model loaded in memory so next request is faster
    }
    # Send to Ollama running on localhost and wait up to 2 minutes
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["response"]


def ask_ollama_vision(image_b64, command):
    # Same as above but also sends a screenshot — uses gemma4 which can see images
    prompt = f"""You are a PC automation agent. The user wants: "{command}"

Look at the screenshot carefully and respond with a JSON array of actions.
Each action must be one of:
- {{"type": "click", "x": 100, "y": 200}}
- {{"type": "type", "text": "hello world"}}
- {{"type": "hotkey", "keys": ["ctrl", "c"]}}
- {{"type": "enter"}}
- {{"type": "wait", "seconds": 1}}
- {{"type": "done", "message": "task complete"}}

Respond ONLY with a valid JSON array. No explanation. No markdown.
Screen coordinates are based on 800x450 scaled resolution.
"""
    payload = {
        "model": "gemma4:latest",  # gemma4 can see images, llama3.1 cannot
        "prompt": prompt,
        "images": [image_b64],     # attach the screenshot here
        "stream": False,
    }
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=300)
    r.raise_for_status()
    return r.json()["response"]


def execute_actions(actions_str):
    # Takes the AI's text response and actually performs the actions on your PC
    try:
        raw = actions_str.strip()
        # Sometimes the AI wraps its response in ```json ... ``` — strip that out
        if "```" in raw:
            parts = raw.split("```")
            raw = parts[1] if len(parts) > 1 else parts[0]
            if raw.startswith("json"):
                raw = raw[4:]  # remove the word "json" from the start
        # Parse the JSON array of actions
        actions = json.loads(raw.strip())
    except Exception:
        # If we can't parse it, show what the AI said and give up
        print(f"[!] Could not parse AI response: {actions_str[:300]}")
        return

    # Get the real screen size so we can scale coordinates correctly
    real_w, real_h = pyautogui.size()
    # The AI thinks the screen is 800x450, so we scale up to real size
    sx = real_w / 800
    sy = real_h / 450

    # Go through each action one by one and execute it
    for action in actions:
        t = action.get("type")  # what kind of action is this?

        if t == "click":
            # Scale the AI's coordinates to real screen coordinates
            x, y = int(action["x"] * sx), int(action["y"] * sy)
            print(f"  -> clicking at ({x}, {y})")
            pyautogui.click(x, y)

        elif t == "type":
            # Type each character with a small delay so it doesn't go too fast
            print(f"  -> typing: {action['text'][:60]}")
            pyautogui.write(action["text"], interval=0.04)

        elif t == "hotkey":
            # Strip any "+" prefix the AI might accidentally add (e.g. "+r" -> "r")
            keys = [k.lstrip("+") for k in action["keys"]]
            print(f"  -> hotkey: {keys}")
            pyautogui.hotkey(*keys)

        elif t == "enter":
            # Press the Enter key
            print(f"  -> pressing Enter")
            pyautogui.press("enter")

        elif t == "scroll":
            x, y = int(action["x"] * sx), int(action["y"] * sy)
            pyautogui.scroll(action.get("amount", 3), x=x, y=y)

        elif t == "wait":
            # Pause so the PC has time to open apps or load pages
            secs = action.get("seconds", 1)
            print(f"  -> waiting {secs}s")
            time.sleep(secs)

        elif t == "done":
            print(f"  -> {action.get('message', 'done')}")

        # Small pause between every action so things don't happen too fast
        time.sleep(0.3)


def hotkey_listener():
    # This runs in a background thread — it listens for F9 to be pressed
    def on_press(key):
        if key == keyboard.Key.f9:
            triggered.set()  # wake up the main loop
    # Keep listening until the program exits
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def ask_command():
    # Shows a small popup box asking what you want to do
    root = tkinter.Tk()
    root.withdraw()  # hide the empty main window, we only want the dialog
    root.attributes("-topmost", True)  # make sure it appears on top of everything
    command = simpledialog.askstring(
        "Lizzarss",
        "What do you want me to do?\n\nTip: start with 'look:' to include a screenshot (slower)",
        parent=root
    )
    root.destroy()  # clean up the tkinter window
    return command.strip() if command else ""  # return empty string if user cancels


def run():
    # Print startup info
    print("=== Lizzarss Agent ===")
    print(f"Hotkey: F9")
    brain = f"Groq ({GROQ_MODEL})" if USE_GROQ else f"Ollama ({OLLAMA_MODEL} @ {OLLAMA_URL})"
    print(f"Brain: {brain}")
    print("Press F9 to activate, Ctrl+C to quit\n")

    # Start the hotkey listener in a background thread so it doesn't block the main loop
    t = threading.Thread(target=hotkey_listener, daemon=True)
    t.start()

    # Main loop — keeps running until you press Ctrl+C
    while True:
        triggered.wait()   # sleep here until F9 is pressed
        triggered.clear()  # reset the signal so it can fire again next time

        try:
            command = ask_command()  # show the popup and get the user's command

            if not command:
                continue  # user pressed Cancel or typed nothing — try again

            if command.lower().startswith("look:"):
                # Vision mode — take a screenshot and let the AI see the screen
                command = command[5:].strip()  # remove the "look:" prefix
                print("[Lizzarss] Taking screenshot...")
                img_b64 = screenshot_b64()
                print("[Lizzarss] Thinking with vision (30-60s)...")
                response = ask_ollama_vision(img_b64, command)  # vision only works with Ollama+gemma4
            else:
                # Fast mode — just send the text command, no screenshot needed
                print("[Lizzarss] Thinking (fast mode)...")
                response = ask_groq(command) if USE_GROQ else ask_ollama_text(command)

            print(f"[Lizzarss] Got response, executing...\n{response[:200]}\n")
            execute_actions(response)  # perform the actions on screen
            print("[Lizzarss] Done. Press F9 for next command.\n")

        except KeyboardInterrupt:
            print("\n[Lizzarss] Stopped.")
            sys.exit(0)
        except Exception as e:
            print(f"[!] Error: {e}\n")


# Only run if this file is executed directly (not imported by another script)
if __name__ == "__main__":
    run()
