# Argus v0.2
# by frankunati
# 20 January 2026

import curses
import psutil
import time
import socket
import asciibars

UPDATE_INTERVAL = 1.0   # seconds
RENDER_DELAY = 0.1      # seconds
BAR_WIDTH = 20			# ASCII bar width

def safe_addstr(win, y, x, text):
    try:
        win.addstr(y, x, text)
    except curses.error:
        pass


def bar(percent, width=BAR_WIDTH):
    percent = max(0, min(100, percent))
    filled = int((percent / 100) * width)
    return "[" + "█" * filled + "-" * (width - filled) + "]"


def get_ipv4():
    interfaces = psutil.net_if_addrs()

    for iface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                if addr.address != "127.0.0.1":
                    return {
                        "interface": iface,
                        "ip": addr.address
                    }
    return None


def collect_metrics(prev_net=None):
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()

    net_delta = None
    if prev_net:
        net_delta = {
            "sent": net.bytes_sent - prev_net.bytes_sent,
            "recv": net.bytes_recv - prev_net.bytes_recv
        }

    return {
        "cpu": cpu,
        "mem": mem,
        "disk": disk,
        "net": net,
        "net_delta": net_delta,
        "ipv4": get_ipv4()
    }


def draw(stdscr, metrics):
    stdscr.erase()
    height, width = stdscr.getmaxyx()

    safe_addstr(stdscr, 1, 2, "ARGUS v0.2")

    safe_addstr(stdscr, 2, 2, "https://github.com/frankunati/Argus")

    # cpu usage bar
    safe_addstr(
        stdscr, 4, 2,
        f"CPU Usage:  {metrics['cpu']:5.1f}% {bar(metrics['cpu'])}"
    )

    # memory usage bar
    mem_pct = metrics["mem"].percent
    safe_addstr(
        stdscr, 5, 2,
        f"Memory:     {mem_pct:5.1f}% {bar(mem_pct)}"
    )

    # disk usage bar
    disk_pct = metrics["disk"].percent
    safe_addstr(
        stdscr, 6, 2,
        f"Disk (/):   {disk_pct:5.1f}% {bar(disk_pct)}"
    )

    # network ID
    if metrics["net_delta"]:
        sent_kb = metrics["net_delta"]["sent"] / 1024
        recv_kb = metrics["net_delta"]["recv"] / 1024
        safe_addstr(
            stdscr, 8, 2,
            f"Net ↑ {sent_kb:6.1f} KB/s  ↓ {recv_kb:6.1f} KB/s"
        )

    if metrics["net_delta"]:
        sent_kb = metrics["net_delta"]["sent"] / 1024
        recv_kb = metrics["net_delta"]["recv"] / 1024
        safe_addstr(
            stdscr, 8, 2,
            f"Net ↑ {sent_kb:6.1f} KB/s  ↓ {recv_kb:6.1f} KB/s"
        )

    ipv4 = metrics.get("ipv4")
    if ipv4:
        safe_addstr(
            stdscr, 9, 2,
            f"IPv4: {ipv4['ip']} ({ipv4['interface']})"
        )
    else:
        safe_addstr(stdscr, 9, 2, "IPv4: Not connected")

    safe_addstr(stdscr, height - 2, 2, "Press Q to quit")
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    last_update = 0
    metrics = None
    prev_net = None

    while True:
        now = time.time()

        if now - last_update >= UPDATE_INTERVAL:
            metrics = collect_metrics(prev_net)
            prev_net = metrics["net"]
            last_update = now

        if metrics is not None:
            draw(stdscr, metrics)

        try:
            key = stdscr.getkey()
            if key.lower() == "q":
                break
        except:
            pass

        time.sleep(RENDER_DELAY)


if __name__ == "__main__":
    curses.wrapper(main)
