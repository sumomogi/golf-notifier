import subprocess

def send_imessage(recipient: str, message: str):
    """Send iMessage to recipient (name as saved in Contacts or phone number)."""
    escaped = message.replace('"', '\\"').replace("'", "'\\''")
    script = f"""
    tell application "Messages"
        set targetService to 1st account whose service type = iMessage
        set targetBuddy to participant "{recipient}" of targetService
        send "{escaped}" to targetBuddy
    end tell
    """
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"iMessage send failed: {result.stderr}")
