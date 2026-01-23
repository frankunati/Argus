# Argus v0.3
# by frankunati
# 23 January 2026

import curses
import time
import asciibars

from metrics import collect_metrics
from network import get_ipv4
from login_monitor import get_logins

UPDATE_INTERVAL = 1.0   # seconds
RENDER_DELAY = 0.1      # seconds
BAR_WIDTH = 20			# ASCII bar width

WINDOW_HEIGHT = 14
WINDOW_WIDTH = 50
WINDOW_Y = 1
WINDOW_X = 2

def safe_addstr(win, y, x, text):
    try:
        win.addstr(y, x, text)
    except curses.error:
        pass


def bar(percent, width=BAR_WIDTH):
    percent = max(0, min(100, percent))
    filled = int((percent / 100) * width)
    return "[" + "█" * filled + "-" * (width - filled) + "]"

def draw(win, metrics):
    win.erase()
    win.box()

    safe_addstr(win, 1, 2, "ARGUS v0.3")	
    safe_addstr(win, 2, 2, "https://www.github.com/frankunati/Argus")

    safe_addstr(win, 4, 2, f"CPU Usage:   {metrics['cpu']:5.1f}%")
    safe_addstr(win, 5, 2, f"Memory:     {metrics['mem'].percent:5.1f}%")
    safe_addstr(win, 6, 2, f"Disk (/):   {metrics['disk'].percent:5.1f}%")

    if metrics.get("net_delta"):
        sent_kb = metrics["net_delta"]["sent"] / 1024
        recv_kb = metrics["net_delta"]["recv"] / 1024
        safe_addstr(win, 7, 2, f"Net ↑ {sent_kb:6.1f} KB/s ↓ {recv_kb:6.1f} KB/s")

    ipv4 = metrics.get("ipv4")
    if ipv4:
        safe_addstr(win, 9, 2, f"IPv4: {ipv4['ip']}")
    else:
        safe_addstr(win, 9, 2, "IPv4: Not connected")

    # display logins
    logins = metrics.get("logins", [])
    safe_addstr(win, 10, 2, "Recent logins:")
    for i, login in enumerate(logins[:WINDOW_HEIGHT - 12]):  # fit in window
        safe_addstr(win, 11 + i, 4, f"- {login}")

    safe_addstr(win, WINDOW_HEIGHT - 2, 2, "Q: Quit")

    win.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    win = curses.newwin(
        WINDOW_HEIGHT,
        WINDOW_WIDTH,
        WINDOW_Y,
        WINDOW_X
    )
    win.nodelay(True)

    last_update = 0
    metrics = None
    prev_net = None
    dirty = True

    while True:
        now = time.time()

        if now - last_update >= UPDATE_INTERVAL:
            metrics = collect_metrics(prev_net)
            metrics["logins"] = get_logins()
            prev_net = metrics["net"]
            last_update = now
            dirty = True

        if dirty and metrics is not None:
            draw(stdscr, metrics)
            dirty = False

        try:
            key = stdscr.getkey()
            if key.lower() == "q":
                break
        except curses.error:
            pass

        time.sleep(RENDER_DELAY)


if __name__ == "__main__":
    curses.wrapper(main)
