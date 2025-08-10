# Voice to tmux

### TL;DR
A small proof-of-concept toy that demonstrates how to send voice commands (and translated voice commands) from a webpage to a terminal program.

### Background
Sometimes, I need to run a program - locally or remotely - that requires typing a lot of prompts or commands.
Recently, that program was Claude Code, which I run remotely over SSH. I wanted a quick way to issue commands using my voice from my Windows machine, so I could “talk” to Claude Code instead of typing - indeed I'm lazy.
Of course, there are other solutions out there, but I wanted to see how I could build something myself.

I tried a few approaches (including Claude Code Hooks and MCP notifications) but none worked out. Eventually, I fell back on the good old tmux trick.
For the uninitiated, tmux (Terminal Multiplexer) is a Linux command-line tool for managing multiple terminal sessions in a single window. More importantly for me, it can inject keystrokes into a session with a simple command—perfect for faking typed input.

#### The core idea:

1. Start a terminal program inside tmux. For example, to run Claude Code:
```# tmux new -A -s claude-session claude```
2.  Open a webpage that captures voice input, sends it to a simple backend, and the backend forwards it to the program via `tmux send-keys` command.

I began with a simple prompt (`initial-prompt.txt`) and built a basic system that accepts text or voice input in the browser, sends it over HTTP to a server, and uses tmux send-keys to feed it into Claude Code.
Later, I extended it: users can speak in their native language, the system uses Google Translate to convert it to English, and then sends the translated text to Claude Code.

And yes - because I’m lazy - I used Claude Code to help write the very system that lets me talk to Claude Code. Which is… amusingly recursive.

<img width="1386" height="980" alt="image" src="https://github.com/user-attachments/assets/80bd2d8a-5726-4c80-b35d-eeeb09af01b4" />
