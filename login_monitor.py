import subprocess

def get_logins():
    try:
        output = subprocess.check_output(
            ["who"],
            text=True
        )
    except subprocess.SubprocessError:
        return []

    sessions = []

    for line in output.strip().split("\n"):
        if not line:
            continue

        parts = line.split()
        sessions.append({
            "user": parts[0],
            "tty": parts[1],
            "time": " ".join(parts[2:5]),
            "source": parts[5] if len(parts) > 5 else "local"
        })

    return sessions
