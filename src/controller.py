import udev_manager
import docker_manager
from typing import AnyStr, Optional
import sys


def print_properties(device_data):
    if device_data.serial:
        print(f"Serial: {device_data.serial}")
    if device_data.vendor_id:
        print(f"Vendor ID: {device_data.vendor_id}")
    if device_data.model_id:
        print(f"Model ID (Product ID): {device_data.model_id}")
    if device_data.path:
        print(f"Path ID: {device_data.path}")
    if device_data.devpath:
        print(f"Devpath: {device_data.devpath}")


def print_devices():
    devices = udev_manager.get_device_list()
    for device in devices:
        print("Device:")
        print_properties(device)
        print("")


def print_rules(filepath: AnyStr):
    with open(filepath) as file:
        file_content = file.read()

    rules = udev_manager.get_device_rules(file_content)

    for key, item in rules:
        print(f"{key}:")
        print(print_properties(item))
        print("")


def check_for_duplicates(file_content, name, path, serial):
    if name in udev_manager.get_names(file_content):
        print("Name is already in use")
        sys.exit()

    if path and path in udev_manager.get_paths(file_content):
        print("path is already in use")
        sys.exit()

    if serial and serial in udev_manager.get_serial_numbers(file_content):
        print("Serial number is already in use")
        sys.exit()


def add_rule(filepath: AnyStr, name: AnyStr, vendor_id: AnyStr, model_id: AnyStr, devpath: AnyStr | None, path: AnyStr | None, serial: AnyStr | None, force=False):
    with open(filepath) as file:
        file_content = file.read()

    if force is False:
        check_for_duplicates(file_content, name, devpath, serial)

    if devpath is None and serial is None:
        raise ValueError("Either devpath or serial has to be specified")

    udev_rule = udev_manager.create_udev_rule(name, serial, devpath, path, vendor_id, model_id)
    file_content = udev_manager.add_rule(file_content, udev_rule)

    with open(filepath, "w") as file:
        file.write(file_content)


def add_rule_docker(filepath: AnyStr, port: int, name: AnyStr, vendor_id: AnyStr, model_id: AnyStr, path: AnyStr | None, serial: AnyStr | None, force=False, docker_filepath: Optional[AnyStr] = None):
    with open(filepath, 'r') as file:
        file_content = file.read()

    if force is False:
        check_for_duplicates(file_content, name, path, serial)

    if path is None and serial is None:
        raise ValueError("Either path or serial has to be specified")

    file_name = docker_manager.create_docker_compose(port, name, docker_filepath)
    start_command = docker_manager.create_start_command(file_name)
    stop_command = docker_manager.create_stop_command(file_name)

    udev_rule = udev_manager.create_startstop_udev_rule(name, start_command, stop_command, serial, path, vendor_id, model_id)
    file_content = udev_manager.add_rule(file_content, udev_rule)

    with open(filepath, "w") as file:
        file.write(file_content)


def remove_rule(filepath: AnyStr, name: AnyStr | None, path: AnyStr | None, serial: AnyStr | None):
    with open(filepath, 'r') as file:
        file_content = file.read()

    if serial:
        file_content = udev_manager.remove_rule_by_serial(file_content, serial)
    elif path:
        file_content = udev_manager.remove_rule_by_path(file_content, path)
    elif name:
        file_content = udev_manager.remove_rule_by_name(file_content, name)

    with open(filepath, 'w') as file:
        file.write(file_content)
