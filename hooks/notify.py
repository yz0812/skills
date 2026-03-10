"""Claude Code hook: task completion notification with duration filter.

Usage:
    PreToolUse: python notify.py mark   — record turn start time
    Stop:       python notify.py        — notify if elapsed > threshold
"""

import os
import platform
import subprocess
import sys
import time
from datetime import datetime

MARKER = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".task_start")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notify-debug.log")
THRESHOLD = 120  # seconds (testing, restore to 120 for production)
MAX_AGE = 3600  # discard stale markers (e.g. after crash)


def log(msg: str) -> None:
    try:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{ts} | {msg}\n")
    except Exception:
        pass


def mark() -> None:
    """Record start time on first tool call of a turn."""
    if os.path.exists(MARKER):
        try:
            age = time.time() - float(open(MARKER).read().strip())
            if age < 60:  # 60 秒内认为是同一轮，保留
                log("MARK: marker already exists, skipped")
                return
            log(f"MARK: stale marker ({age:.0f}s old), overwriting")
        except Exception:
            log("MARK: corrupt marker, overwriting")
    with open(MARKER, "w") as f:
        f.write(str(time.time()))
    log(f"MARK: wrote start time to {MARKER}")


def notify() -> None:
    """Notify if elapsed time exceeds threshold."""
    log(f"NOTIFY: called, checking marker at {MARKER}")
    if not os.path.exists(MARKER):
        log("NOTIFY: no marker file, exiting")
        return
    try:
        start = float(open(MARKER).read().strip())
        os.remove(MARKER)
        log(f"NOTIFY: read start={start}, marker removed")
    except Exception as e:
        log(f"NOTIFY: error reading marker: {e}")
        return

    elapsed = time.time() - start
    log(f"NOTIFY: elapsed={elapsed:.1f}s, threshold={THRESHOLD}s, max_age={MAX_AGE}s")
    if elapsed > MAX_AGE or elapsed < THRESHOLD:
        log(f"NOTIFY: skipped (out of range)")
        return

    minutes, seconds = int(elapsed // 60), int(elapsed % 60)
    msg = f"Task completed ({minutes}m{seconds:02d}s)"
    title = "Claude Code"
    log(f"NOTIFY: sending notification: {msg}")

    os_name = platform.system()
    if os_name == "Windows":
        _windows(title, msg)
    elif os_name == "Darwin":
        _macos(title, msg)


def _windows(title: str, message: str) -> None:
    ps = (
        "[Windows.UI.Notifications.ToastNotificationManager,"
        " Windows.UI.Notifications, ContentType = WindowsRuntime] > $null;"
        "[Windows.Data.Xml.Dom.XmlDocument,"
        " Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] > $null;"
        "$xml = New-Object Windows.Data.Xml.Dom.XmlDocument;"
        "$xml.LoadXml('"
        "<toast duration=\"long\"><visual><binding template=\"ToastGeneric\">"
        f"<text>{title}</text>"
        f"<text>{message}</text>"
        "</binding></visual></toast>');"
        "$t = [Windows.UI.Notifications.ToastNotification]::new($xml);"
        "[Windows.UI.Notifications.ToastNotificationManager]"
        "::CreateToastNotifier('{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe').Show($t)"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            capture_output=True, text=True, timeout=10,
            creationflags=0x08000000,
        )
        if result.returncode != 0:
            log(f"WINDOWS: powershell failed (rc={result.returncode}): {result.stderr.strip()}")
        else:
            log("WINDOWS: toast sent successfully")
    except Exception as e:
        log(f"WINDOWS: exception: {e}")


def _macos(title: str, message: str) -> None:
    subprocess.Popen([
        "osascript", "-e",
        f'display notification "{message}" with title "{title}"',
    ])


if __name__ == "__main__":
    # Drain stdin to avoid blocking (hooks receive JSON on stdin)
    try:
        sys.stdin.read()
    except Exception:
        pass

    argv_info = f"argv={sys.argv}"
    log(f"ENTRY: {argv_info}")

    if len(sys.argv) > 1 and sys.argv[1] == "mark":
        mark()
    else:
        notify()
