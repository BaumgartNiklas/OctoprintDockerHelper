udev_rules_data = '''
SUBSYSTEM=="tty", ATTRS{idVendor}=="1973",  ATTRS{idProduct}=="5927", ATTRS{devpath}=="1.1", SYMLINK+="Printer1"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1973",  ATTRS{idProduct}=="5927", ATTRS{serial}=="3940855329", SYMLINK+="Printer2"
SUBSYSTEM=="tty", ATTRS{serial}=="ryvk87g4", SYMLINK+="Printer7"
SUBSYSTEM=="tty", ATTRS{devpath}=="1.5", SYMLINK+="Printer8"

SUBSYSTEM=="tty", ENV{ID_VENDOR_ID}=="m78", ENV{ID_MODEL_ID}=="ab4g", ENV{ID_SERIAL}=="kise", SYMLINK+="Printer3", ACTION=="add", RUN+="start"
SUBSYSTEM=="tty", ENV{ID_VENDOR_ID}=="m78", ENV{ID_MODEL_ID}=="ab4g", ENV{ID_SERIAL}=="kise", ACTION=="remove", RUN+="stop"
SUBSYSTEM=="tty", ENV{ID_SERIAL}=="kpl6", SYMLINK+="Printer4", ACTION=="add", RUN+="start"
SUBSYSTEM=="tty", ENV{ID_SERIAL}=="kpl6", ACTION=="remove", RUN+="stop"

SUBSYSTEM=="tty", ENV{ID_VENDOR_ID}=="m78", ENV{ID_MODEL_ID}=="ab4g", ENV{ID_PATH}=="UsbPathTo1", SYMLINK+="Printer5", ACTION=="add", RUN+="start"
SUBSYSTEM=="tty", ENV{ID_VENDOR_ID}=="m78", ENV{ID_MODEL_ID}=="ab4g", ENV{ID_PATH}=="UsbPathTo1", ACTION=="remove", RUN+="stop"
SUBSYSTEM=="tty", ENV{ID_PATH}=="UsbPathTo2", SYMLINK+="Printer6", ACTION=="add", RUN+="start"
SUBSYSTEM=="tty", ENV{ID_PATH}=="UsbPathTo2", ACTION=="remove", RUN+="stop"
'''

docker_compose_sample = \
'''version: '2.4'
name: Printer1

services:
  octoprint:
    image: octoprint/octoprint
    restart: unless-stopped
    ports:
      - 5000:80
    devices:
      - /dev/Printer1:/dev/ttyUSB0
    volumes:
      - octoprint:/octoprint

volumes:
  octoprint:
'''
