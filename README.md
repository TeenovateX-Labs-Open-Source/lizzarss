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

You need two things: **Python** and **Ollama**.

**Ollama** is the AI brain. It runs on your own computer so nothing gets sent anywhere. Download it at [ollama.com/download](https://ollama.com/download). Free, takes 2 minutes to install.

After installing Ollama, open your terminal and run:

```bash
ollama pull llama3.1
```

This downloads the AI model (~5GB). Do it once, never again.

Then install the Python stuff:

```bash
pip install pyautogui pillow requests pynput
```

Open `agent.py`, find line 9, change it to:

```python
OLLAMA_URL = "http://localhost:11434"
```

Then run it:

```bash
python agent.py
```

---

## Using it

Press **F9** anywhere on your screen. Type your command. Hit OK.

Some things you can try:

```
open chrome
open notepad and type my name is David
select all and delete
open calculator
copy everything on screen
```

---

## The two modes

**Normal mode**: just type your command. Fast, about 5 seconds. The AI uses its brain to figure out what to do without looking at your screen.

**Look mode**: add `look:` before your command. The AI takes a screenshot first, sees exactly what's on your screen, then acts. Slower (30-60 seconds) but smarter for complicated stuff.

```
look: click the submit button on this page
look: what app is open right now, close it
```

---

## It's not perfect (yet)

Sometimes it clicks in the wrong place. Sometimes it misses a step. That's because the AI is guessing what to do based on your words. It gets better the more specific you are.

Bad: `open my thing`
Good: `open notepad and type hello`

When it messes up, just press F9 again and correct it.

---

## What you need

- Windows 10 or 11
- Python 3.10 or newer
- About 5GB free space for the AI model
- Ollama installed

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

## Built by

David.

If you build something cool with this, let me know.
