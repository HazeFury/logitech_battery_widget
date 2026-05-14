import subprocess


def get_mouse_battery() -> int:
    """
    Executes the 'solaar show' command to get a dump of all power devices.
    Returns the mouse battery level as int, or -1 on error.
    """
    try:
        # capture_output=True grabs stdout and stderr
        # text=True returns the output as a string instead of bytes
        process = subprocess.run(
            ['solaar', 'show'],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError:
        return -1

    for line in process.stdout.split('\n'):
        clean_line = line.strip()
        if clean_line.startswith("Battery:"):
            parts = clean_line.split()
            battery_value = parts[1].replace("%,", "")
            return int(battery_value)
    return -1


def get_headset_battery() -> int:
    """
    Executes headsetcontrol to fetch the battery level.
    Returns the headset battery level as int, or -1 on error.
    """
    try:
        process = subprocess.run(
            ['headsetcontrol', '-b'],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError:
        return -1

    for line in process.stdout.split('\n'):
        clean_line = line.strip()
        if clean_line.startswith("Level:"):
            parts = clean_line.split()
            if len(parts) >= 2:
                return int(parts[1].replace('%', ''))
    return -1


if __name__ == "__main__":
    mouse_value = get_mouse_battery()
    headset_value = get_headset_battery()

    mouse_battery = f"{mouse_value}%" if mouse_value != -1 else "--"
    headset_battery = f"{headset_value}%" if headset_value != -1 else "--"
    print(f"Mouse battery = {mouse_battery}")
    print(f"Headset battery = {headset_battery}")
