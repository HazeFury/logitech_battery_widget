# Logitech Battery Widget

A simple script to show the battery level of your wireless peripheral (mouse, headset, keyboard). Designed to work with Logitech hardware, you should be able to adapt it with your own peripherals.

<div align="center">
<br>
  <img src="./illustration.png" alt="illustration" width="400" />

  <br>
</div>

## How it works

1. The Python script fetch battery data and print the output. I use the command `solaar show` for the mouse and `headsetcontrol -b` for the headset.

2. On GNOME environment, the plugins **Executor** allows you to run the script at regular intervals and you can choose where to display it.

## Installation

You will need these to run the script :

- Python 3.10 or higher
- solaar (https://github.com/pwr-Solaar/Solaar)
- HeadsetControl (https://github.com/Sapd/HeadsetControl)

Once everything is installed :

### step 1 : clone this repository and test the script

```bash
    git clone https://github.com/HazeFury/logitech_battery_widget

    cd logitech_battery_widget

    # I recommand to copy the script in a proper "scripts" folder near your home folder
    cp get_battery_level.py ~/scripts

    # Make the script executable
    chmod +x ~/scripts/get_battery_level.py

    # Verify it works well in your terminal
    ~/scripts/get_battery_level.py
    # You should see something like : 🎧 72% | 🖱️ 50%
```

### step 2 : install Extension Manager plugin and Executor

If you are using a GNOME environment, you can install "**Extension Manager**" application on your desktop. Then :

1. Open your GNOME application menu and launch the Extensions Manager application (the icon is a small blue puzzle piece).

2. Go to the Browse tab at the top of the window.

3. In the search bar, type Executor.

4. Click the "Install" button next to the Executor extension (created by raujonas or similar).

5. Go back to the Installed tab. You should see Executor there. Click the small gear icon ⚙️ next to it to open its settings.

### step 3 : Setup Executor to run the script

In the Executor configuration window, you can define your widget:

**Command**: This is where you put the absolute path to your script.
e.g :
`/home/YOURNAME/scripts/battery_widget.py`

**Interval**: Set this to 60 seconds (or more). Note that the call to Solaar is somewhat resource-intensive; you should definitely not leave the interval at the default (often 1 or 5 seconds) or you risk slowing down your system. (I will fix that in V2)

**Location**: You can choose where to place it (usually Right or Center in the Top Bar).

**As soon as you confirm, you should see your little emojis and battery percentages appear directly in your GNOME bar at the top of your screen.**

<br>

## Troubleshooting

I had trouble installing 'HeadsetControl' because I was using Debian 12, and this caused problems compiling the project because it required Debian 13 to have GCC 13.

If this happens to you, you need to use a Docker container of an older version (Unbuntu 22.04) and install GCC 13, then force the compiler to include the C++ library in the executable.

Here's how it worked for me :

```bash
mkdir temp_folder && cd temp_folder
docker run -it -v $(pwd):/workspace ubuntu:22.04 bash

# inside the docker container
apt update
apt install -y software-properties-common wget build-essential git cmake libhidapi-dev
add-apt-repository ppa:ubuntu-toolchain-r/test -y
apt update
apt install -y gcc-13 g++-13
cd /tmp
git clone https://github.com/Sapd/HeadsetControl.git
cd HeadsetControl
mkdir build && cd build
export CC=gcc-13
export CXX=g++-13
export CXXFLAGS="-static-libstdc++ -static-libgcc"
export LDFLAGS="-static-libstdc++ -static-libgcc"
cmake ..
make
cp headsetcontrol /workspace/
cp 70-headsets.rules /workspace/
exit

sudo mv headsetcontrol /usr/local/bin/
sudo cp 70-headsets.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Unplug the dongle from your headset, plug it back in, and launch a simple:

```bash
headsetcontrol -b
```

You should see your headset data with the battery level :)
