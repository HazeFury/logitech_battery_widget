#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

STATE_FILE = Path("/dev/shm/headset_light.state")
SCRIPT_PATH = Path(__file__).resolve()


def read_light_state() -> bool:
    """Reads the cached state from memory. Defaults to False if missing."""
    if not STATE_FILE.exists():
        return False
    try:
        return STATE_FILE.read_text().strip() == "1"
    except OSError:
        return False


def write_light_state(is_on: bool) -> None:
    """Persists the current light state into shared memory."""
    try:
        STATE_FILE.write_text("1" if is_on else "0")
    except OSError:
        pass


def set_hardware_light(is_on: bool) -> bool:
    """Executes headsetcontrol to turn LED on (1) or off (0)."""
    val = "1" if is_on else "0"
    try:
        subprocess.run(
            ["headsetcontrol", "-l", val], capture_output=True, check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def handle_toggle() -> None:
    """Toggles state, applies hardware change, and updates persistence."""
    current_state = read_light_state()
    new_state = not current_state

    # Send command to headset and update cache on success
    if set_hardware_light(new_state):
        write_light_state(new_state)


def handle_display() -> None:
    """Prints formatted output with Pango markup for Argos."""
    is_on = read_light_state()
    status_label = (
        '<span color="#2ECC71"><b>ON</b></span>'
        if is_on
        else '<span color="#E74C3C"><b>OFF</b></span>'
    )
    action_label = "Éteindre les LED" if is_on else "Allumer les LED"

    print(f"🎧 Light: {status_label} | use_markup=true")

    print("---")

    argos_params = (
        f'bash="{SCRIPT_PATH}" param1="toggle" terminal=false refresh=true'
    )
    print(f"💡 {action_label} | {argos_params}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "toggle":
        handle_toggle()
    else:
        handle_display()
