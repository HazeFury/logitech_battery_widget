import subprocess


def get_mouse_battery() -> int:
    """
    Executes the 'solaar show' command to get a dump of all power devices.
    Returns the mouse battery level as int or -1 if not found.
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


if __name__ == "__main__":
    mouse_value = get_mouse_battery()

    mouse_battery = f"{mouse_value}%" if mouse_value != -1 else "--"
    print(f"Mouse battery = {mouse_battery}")
