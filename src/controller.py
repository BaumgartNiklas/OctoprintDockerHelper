import sys
import udev_manager
import docker_manager
from typing import AnyStr, Optional


def print_properties(device_data):
    """Prints the properties of an usb device

    Args:
        device_data: device data object
    """
    if device_data.serial:
        print(f"Serial: {device_data.serial}")
    if device_data.vendor_id:
        print(f"Vendor ID: {device_data.vendor_id}")
    if device_data.model_id:
        print(f"Model ID/Product ID: {device_data.model_id}")
    if device_data.path:
        print(f"Path ID: {device_data.path}")
    if device_data.devpath:
        print(f"Devpath: {device_data.devpath}")


def print_devices():
    """Prints the device properties of all currently connected usb devices."""
    devices = udev_manager.get_device_list()
    for device in devices:
        print("Device:")
        print_properties(device)
        print("")


def print_rules(filepath: AnyStr):
    """Prints udev rules present in the specified file

    Args:
        filepath: filepath of the rule file
    """
    with open(filepath) as file:
        file_content = file.read()

    rules = udev_manager.get_device_rules(file_content)

    for key, item in rules.items():
        print(f"{key}:")
        print_properties(item)
        print("")


def check_for_duplicates(file_content: AnyStr, name: AnyStr, path: AnyStr, serial: AnyStr) -> (bool, AnyStr):
    """Checks if the specified name, path or serial number is present in the rule file.

    Args:
        file_content: content of the rule file as a string
        name: name (symlink name) to check for
        path: path (id path or devpath) to check for
        serial: serial number to check for

    Returns:
        (bool, str) If one of the attributes is present in the file, true is returned, otherwise false.
        The string contains the name of the attribute (name, path, serial) that was found or is empty if none were found.
    """
    if name in udev_manager.get_names(file_content):
        return True, "name"

    if path and path in udev_manager.get_paths(file_content):
        return True, "path"

    if serial and serial in udev_manager.get_serial_numbers(file_content):
        return True, "Serial"

    return False, ''


def add_rule(filepath: AnyStr, name: AnyStr, vendor_id: AnyStr, model_id: AnyStr, devpath: Optional[AnyStr], path: Optional[AnyStr], serial: Optional[AnyStr], force: bool = False):
    """Adds a rule to the udev rule file.
    Either the devpath, path or serial has to be specified.
    Checks if the given name, serial, path or devpath is already used in another rule. If another rule is found,
    it raises value error.

    Args:
        filepath: filepath of the udev rule file
        name: name (symlink name) of the new rule
        vendor_id: vendor id to use in the rule
        model_id: model id to use in the rule
        devpath: devpath to use in the rule
        path: id path to use in the rule
        serial: serial number to use in the rule
        force: force the new rule to be added and already existing duplicates.

    Raises:
        ValueError: if devpath, serial and path are None
        ValueError: if devpath, serial or path are already in use
    """
    if devpath is None and serial is None and path is None:
        print("Either devpath or serial or path has to be specified")
        sys.exit()

    with open(filepath) as file:
        file_content = file.read()

    if force is False:
        has_attr, attr_type = check_for_duplicates(file_content, name, devpath, serial)
        if has_attr:
            print(f"{attr_type} is already in use")
            sys.exit()

    udev_rule = udev_manager.create_udev_rule(name, serial, devpath, path, vendor_id, model_id)
    file_content = udev_manager.add_rule(file_content, udev_rule)

    with open(filepath, "w") as file:
        file.write(file_content)


def add_rule_docker(filepath: AnyStr, port: int, name: AnyStr, vendor_id: AnyStr, model_id: AnyStr, path: Optional[AnyStr], serial: Optional[AnyStr], force=False, docker_filepath: Optional[AnyStr] = None):
    """Adds a rule to the udev rule file.
    Either the path or serial has to be specified.
    Checks if the given name, serial oa path is already used in another rule. If another rule is found,
    it raises value error.
    Additionally, a docker compose file is created which provides Octoprint on the specified port.
    Each new rule is split into a 'connect' and 'disconnect' rule which starts or stops the docker container respectively.

    Args:
        filepath: filepath of the udev rule file
        port: Port under which the octoprint instance should be accessible
        name: name (symlink name) of the new rule
        vendor_id: vendor id to use in the rule
        model_id: model id to use in the rule
        path: id path to use in the rule
        serial: serial number to use in the rule
        force: force the new rule to be added and already existing duplicates.
        docker_filepath: file path to save the docker compose file
    """
    if path is None and serial is None and path is None:
        print("Either path or serial has to be specified")

    with open(filepath, 'r') as file:
        file_content = file.read()

    if force is False:
        has_attr, attr_type = check_for_duplicates(file_content, name, path, serial)
        if has_attr:
            print(f"{attr_type} is already in use")
            sys.exit()

    file_name = docker_manager.create_docker_compose(port, name, docker_filepath)
    start_command = docker_manager.create_start_command(file_name)
    stop_command = docker_manager.create_stop_command(file_name)

    udev_rule = udev_manager.create_startstop_udev_rule(name, start_command, stop_command, serial, path, vendor_id, model_id)
    file_content = udev_manager.add_rule(file_content, udev_rule)

    with open(filepath, "w") as file:
        file.write(file_content)


def remove_rule(filepath: AnyStr, name: Optional[AnyStr], path: Optional[AnyStr], serial: Optional[AnyStr]):
    """Removes a rule from an udev rule file.
    Only one of the optional parameters has to be specified for the corresponding rules to be removed.

    Args:
        filepath: filepath of the udev rule file
        name: name (symlink name) of the new rule
        path: id path to use in the rule
        serial: serial number to use in the rule
    """
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
