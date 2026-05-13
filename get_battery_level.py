import subprocess
import sys


def fetch_solaar_data() -> str:
    """
    Executes the 'solaar show' command to get a dump of all power devices.
    Returns the standard output as a raw string.
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
        return process.stdout
    except subprocess.CalledProcessError as error:
        print(f"Failed to execute upower: {error}")
        sys.exit(1)


def extract_device_metrics(raw_data: str) -> None:
    """
    Parses the raw string from UPower to find specific metrics
    like the model name and battery percentage.
    """
    lines = raw_data.split('\n')

    for line in lines:
        cleaned_line = line.strip()
        # Basic parsing strategy: look for key strings
        if cleaned_line.startswith("Codename"):
            print(f"Device Found: {cleaned_line}")
        elif cleaned_line.startswith("Battery:"):
            print(f"Battery Level: {cleaned_line}")
            return


if __name__ == "__main__":
    power_dump = fetch_solaar_data()
    if power_dump:
        extract_device_metrics(power_dump)
