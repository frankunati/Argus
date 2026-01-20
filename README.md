# Argus - Linux-based System Monitor

Argus is a lightweight, terminal-based system monitor for Linux distros. It's written in Python and  uses 'psutil'
for fetching usage data and 'curses' for terminal handling.

------------------------------------

# Features

- Live CPU, Memory, and Disk usage monitoring
- Network upload/download rates
- IPv4 address detection (detects your machine's local IP, for now)
- Minimalist Terminal UI (will be adding more 'pizazz' to it soon)

------------------------------------

# Device Requirements

- Python 3
- Linux-based OS
- Python packages (required):
	- 'psutil'
	- 'asciibars'

Open your terminal and install dependencies using:
pip install psutil, asciibars
