import subprocess

def send_imessage(recipient: str, message: str):
    """Send iMessage to recipient (phone number in E.164 format, e.g. +818066626916)."""
    escaped = message.replace('"', '\\"')
    result = subprocess.run([
        "osascript",
        "-e", "tell application \"Messages\"",
        "-e", "set svc to 1st service whose service type = iMessage",
        "-e", f'send "{escaped}" to buddy "{recipient}" of svc',
        "-e", "end tell"
    ], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"iMessage send failed: {result.stderr}")
