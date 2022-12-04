# CLI for easier Octoprint Docker instances

## Description

This is a small python command line interface to make the creation of Octoprint instances using Docker and udev rules
easier. It is specifically made to support udev rules that can start and stop the Docker container. This helps to
avoid problems when the 3d printer is not connected, since Docker does not deal well with dynamically plugged USB
devices (also it saves resources while the printer is unplugged).
Currently, setups including webcams are not possible, but I plan on implementing support in the future.

For further details regarding Octoprint visit their [Website](https://octoprint.org/) or [GitHub](https://github.com/OctoPrint/OctoPrint)([Docker Container](https://github.com/OctoPrint/octoprint-docker)).

## Getting Started
1. Install Docker and Docker Compose
2. Install Python3 3.6 or newer
3. Install [pyudev](https://github.com/pyudev/pyudev) `pip install pyudev`
4. Download and extract the [latest release](https://github.com/BaumgartNiklas/OctoprintDockerHelper/releases/download/v1.0.0/OctoprintDockerHelper.zip)

## How to use
To use the command line interface, execute the 'octodocker.py' in the extracted folder.\
`python3 octodocker.py`\
The script provides a help page to get you started.\
The available options are:\
* devices: Shows all currently connected devices and their attributes
* rules: Shows all your current udev rules
* add: adds a new rule
* remove: removes a rule