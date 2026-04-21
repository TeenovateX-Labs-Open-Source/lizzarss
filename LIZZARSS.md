# Lizzarss — Local AI PC Automation Agent

Tell your computer what to do in plain English. Lizzarss uses a local AI model (via Ollama) to understand your command and execute it — clicking, typing, opening apps, filling forms — all automatically.

No cloud. No subscriptions. Runs entirely on your machine.

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/download) installed locally
- A vision-capable model pulled in Ollama

---

## Setup

**1. Install Ollama**

Download from [ollama.com/download](https://ollama.com/download) and install it.

**2. Pull a model**

Open terminal and run:
```bash
ollama pull gemma4
```
This downloads the AI brain (~9.6GB). Do this once.

For a lighter/faster option:
```bash
ollama pull llama3.1
```

**3. Clone / download Lizzarss**

Put `agent.py` and `requirements.txt` in a folder.

**4. Install Python dependencies**
```bash
pip install pyautogui pillow requests pynput
```

**5. Point Lizzarss at your local Ollama**

Open `agent.py` and change line 9:
```python
OLLAMA_URL = "http://localhost:11434"
```

---

## Run it

```bash
python agent.py
```

---

## Usage

1. Press **F9** anywhere on your screen
2. A popup appears — type what you want done
3. Hit OK — Lizzarss executes it

**Two modes:**

| Mode | How to trigger | Speed | Best for |
|------|---------------|-------|---------|
| Fast | Type normally | ~5-10s | Opening apps, typing text, shortcuts |
| Vision | Start command with `look:` | ~30-60s | Tasks that need to see your screen |

**Examples:**
```
open chrome and go to youtube
fill in the form with my name David and email david@gmail.com
look: click the submit button on this page
open notepad and type a to-do list for today
copy all the text on screen
```

---

## How it works

```
F9 pressed
    → popup appears
    → you type command
    → screenshot taken (vision mode) or skipped (fast mode)
    → sent to local Ollama AI
    → AI returns list of actions (click, type, hotkey...)
    → Lizzarss executes them on your screen
```

---

## Troubleshooting

**Agent does nothing after command**
- Make sure Ollama is running: open terminal and type `ollama list`
- If empty, pull a model: `ollama pull llama3.1`

**Clicks in wrong place**
- Use `look:` prefix so the AI can see your screen layout

**Too slow**
- Use `llama3.1` instead of `gemma4` for fast mode (edit `agent.py` line 10)
- Avoid vision mode unless necessary

---

Built by David. Powered by Ollama + Gemma/LLaMA.
