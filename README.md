# CLI for easier Octoprint Docker instances

## Description

This is a small python command line interface to make the creation of Octoprint instances using Docker and udev rules
easier. It is specifically made to support udev rules that can start and stop the Docker container. This helps to
avoid problems when the 3d printer is not connected, since Docker does not deal well with dynamically plugged USB
devices (also it saves resources while the printer is unplugged).
Currently, setups including webcams are not possible, but I plan on implementing support in the future.

## Usage


### Warning
**while some parts of the software are tested, the test cases do not cover everything and I did not put a lot of 
effort into testing on my own machine so your mileage may vary**