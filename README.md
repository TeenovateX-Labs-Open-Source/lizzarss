# Lizzarss

Your computer does what you tell it. In plain English.

Not "click File > New > Save As..." nonsense. Just: *"open notepad and write my assignment intro"* and it does it. While you watch.

---

## Okay but what is this actually

You press **F9**. A small box pops up. You type what you want your computer to do. It does it.

That's it.

Open apps. Type stuff. Fill forms. Copy things. Whatever you'd normally do with your hands, Lizzarss does it for you.

I built this because I kept doing the same boring things on my PC over and over. Opening the same apps, typing the same things, filling the same forms. So I made something that handles all of that while I just sit back.

---

## Watch it work

![Lizzarss popup](screenshots/popup.png)

![Result in Notepad](screenshots/result.png)

You type:
```
open a new notepad and type hello world
```

And your computer goes:
- opens Run dialog
- types "notepad"
- presses Enter
- waits for it to open
- types "hello world"

All by itself. In about 5 seconds.

---

## How to get it running

Pick one option depending on your PC.

---

### Option 1: Groq (easiest works on any PC, no downloads)

Groq is a free cloud AI. No GPU needed, no 5GB downloads, works on even the oldest laptop.

1. Get a free API key at [console.groq.com](https://console.groq.com) (takes 1 minute)
2. Open `agent.py` and paste your key on line 18:
```python
GROQ_API_KEY = "paste_your_key_here"
```
3. Install dependencies:
```bash
pip install pyautogui pillow requests pynput
```
4. Run:
```bash
python agent.py
```

That's it. No model downloads. Works on 4GB RAM.

---

### Option 2: Ollama (fully local nothing leaves your machine)

If you want everything to run on your own PC with no internet dependency:

1. Install [Python 3.10+](https://www.python.org/downloads/) if you don't have it
2. Download [Ollama](https://ollama.com/download) and install it
3. Pull a model (download once, ~5GB):
```bash
ollama pull llama3.1
```
4. Install dependencies:
```bash
pip install pyautogui pillow requests pynput
```
5. Make sure `GROQ_API_KEY` in `agent.py` line 18 is empty (default), then run:
```bash
python agent.py
```

---

## Using it

Press **F9** anywhere on your screen. A box pops up. Type your command. Hit OK.

```
open chrome
open notepad and type my name is David
select all and delete
open calculator
copy everything on screen
press ctrl+z three times
```

---

## The two modes

**Normal mode** just type your command. Fast (~5 seconds). Best for opening apps, typing, shortcuts.

**Look mode** add `look:` before your command. Lizzarss takes a screenshot first so the AI can literally see your screen before acting. Slower (30-60s) but smarter for anything visual.

```
look: click the submit button on this page
look: what app is open right now, close it
look: fill in the first form field with my name
```

---

## It's not perfect (yet)

Sometimes it clicks in the wrong place. Sometimes it misses a step. It gets better the more specific you are.

Bad: `open my thing`
Good: `open notepad and type hello`

When it messes up, press F9 again and correct it.

---

## What you need

- Windows 10 or 11
- [Python 3.10+](https://www.python.org/downloads/)
- Either a free [Groq API key](https://console.groq.com) OR [Ollama](https://ollama.com/download) installed locally

---

## Useful resources

- [Lizzarss on GitHub](https://github.com/TeenovateX-Labs-Open-Source/lizzarss) the full source code, fork it from here
- [Get a free Groq API key](https://console.groq.com) fastest way to get started, no downloads needed
- [Download Ollama](https://ollama.com/download) run AI locally on your PC
- [Download Python](https://www.python.org/downloads/) needed to run Lizzarss
- [pyautogui docs](https://pyautogui.readthedocs.io) the library that controls your mouse and keyboard
- [Groq model list](https://console.groq.com/docs/models) swap to a different AI model if you want
- [Ollama model library](https://ollama.com/library) all models you can run locally

---

## Ideas to build on this

This is just the starting point. Here's what you could add:

**Browser control:** make it open Chrome and actually navigate websites. Search Google, scroll Twitter, fill forms on any site, read your emails out loud.

**Morning routine:** save a sequence of tasks under one word. Say "morning" and it opens your browser, checks Gmail, loads your current project, all by itself.

**Form filler:** store your name, email, address once. Then just say "fill this form" on any website and it populates everything automatically.

**Voice trigger:** instead of pressing F9, just say "hey lizzarss" out loud and the popup appears. Fully hands-free.

**App-specific shortcuts:** teach it your workflow. "push my code" runs git add, commit, push. "new component" creates a file and opens it in VS Code.

**Scheduled tasks:** run something every morning at 8am without you touching anything. Open your to-do list, clear your downloads folder, back up your files.

**Multi-screen awareness:** take a screenshot, let the AI describe everything it sees, then decide what to click based on what's actually on screen.

**Phone mirroring:** combine with Android screen mirroring to control your phone from your PC with plain English commands.

If you build any of these, share it.

---

## The Challenge

There is an open challenge to extend Lizzarss into something nobody has built yet.

See [CHALLENGE.md](CHALLENGE.md) for full details.

---

## Built by

David.

If you build something cool with this, let me know.
