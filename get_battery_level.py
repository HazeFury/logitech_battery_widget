#!/usr/bin/env python3

import re
import subprocess

import pydbus


def get_mouse_battery() -> int:
    """
    Connects directly to the user D-Bus to read Solaar's notification tooltip.
    This is extremely fast and non-blocking (I/O bound optimized).
    Returns the mouse battery level as int, or -1 on error.
    """
    try:
        # Connect to the session bus (user-level bus)
        bus = pydbus.SessionBus()

        # Access the specific Solaar object on the bus
        solaar_object = bus.get(
            "io.github.pwr_solaar.solaar",
            "/org/ayatana/NotificationItem/indicator_solaar",
        )

        # Read the property we found during introspection
        tooltip_desc = solaar_object.IconAccessibleDesc

        # Example of tooltip_desc: "G502 X PLUS: Battery: 49% (discharging..."
        # We use a simple regex to extract the first
        # group of digits followed by '%'
        match = re.search(r"(\d+)%", tooltip_desc)

        if match:
            return int(match.group(1))
    except Exception:  # noqa: BLE001, S110
        # Silently catch D-Bus errors (e.g., Solaar is not running)
        pass

    return -1


def get_headset_battery() -> int:
    """
    Executes headsetcontrol to fetch the battery level.
    Returns the headset battery level as int, or -1 on error.
    """
    try:
        process = subprocess.run(
            ["headsetcontrol", "-b"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        return -1

    for line in process.stdout.split("\n"):
        clean_line = line.strip()
        if clean_line.startswith("Level:"):
            parts = clean_line.split()
            if len(parts) >= 2:
                return int(parts[1].replace("%", ""))
    return -1


def format_status_bar_output(mouse_lvl: int, headset_lvl: int) -> None:
    """
    Formats the battery levels into a single concise string for the status bar.
    Using Unicode characters for visual feedback.
    """
    mouse_str = f"{mouse_lvl}%" if mouse_lvl != -1 else "--"
    headset_str = f"{headset_lvl}%" if headset_lvl != -1 else "--"

    # Prints a single line: 🎧 64% | 🖱️ 80%
    print(f"🎧 {headset_str} | 🖱️ {mouse_str}")


if __name__ == "__main__":
    mouse_value = get_mouse_battery()
    headset_value = get_headset_battery()
    format_status_bar_output(mouse_value, headset_value)
