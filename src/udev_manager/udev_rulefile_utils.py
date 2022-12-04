import re
from typing import AnyStr
from .device_data import DeviceData


def get_serial_numbers(file_content: AnyStr) -> list:
    """Gets all serial numbers currently used in the udev file

    Args:
        file_content: file content of the udev configuration file

    Returns:
        List of all serial numbers used
    """
    return re.findall('(?!.*remove)(?:ATTRS{serial}|ENV{ID_SERIAL})=="(.*?)"(?!.*remove)', file_content)


def get_paths(file_content: AnyStr) -> list:
    """Gets all usb paths and devpaths currently used in the udev file

    Args:
        file_content: file content of the udev configuration file

    Returns:
        List of all paths and devpaths
    """
    return re.findall('(?!.*remove)(?:ATTRS{devpath}|ENV{ID_PATH})=="(.*?)"(?!.*remove)', file_content)


def get_names(file_content: AnyStr) -> list:
    """Gets all names (Symlink names) currently used in the udev file

    Args:
        file_content: file content of the udev configuration file

    Returns:
        List of all names (symlinks) used
    """
    return re.findall('SYMLINK\+="(.*?)"', file_content)


def get_device_attribute(search_string: AnyStr, text: AnyStr, capture_group: int = 1) -> AnyStr | None:
    """Searches for the specified regex expression in the text and returns the capture group.
    If no match is found, None is returned.

    Args:
        text: text to search trough
        search_string: regex search string
        capture_group: number of the capture group to return

    Returns:
        string with the value of the first capture group or None
    """
    attribute = re.search(search_string, text)
    if attribute:
        attribute = attribute.group(capture_group)
    return attribute


def get_device_rules(file_content: AnyStr) -> dict:
    """Gets all devices which currently have a rule in the file.
    For each device, the name, vendor id, product id (model id), serial number, devpath and path as stored. If a device does not
    have an entry for the respective item, it is set to None.

    Args:
        file_content: file content of the udev configuration file

    Returns:
        Dictionary mapping the device names to their respective attributes.
        The attributes are stored as a DeviceData object.
    """
    devices = {}
    entries = re.findall(".*SYMLINK.*\n", file_content)

    for entry in entries:
        name = get_device_attribute('SYMLINK\+="(.*?)"', entry)
        vendor = get_device_attribute('(?:ATTRS{idVendor}|ENV{ID_VENDOR_ID})=="(.*?)"', entry)
        product = get_device_attribute('(?:ATTRS{idProduct}|ENV{ID_MODEL_ID})=="(.*?)"', entry)
        serial = get_device_attribute('(?:ATTRS{serial}|ENV{ID_SERIAL})=="(.*?)"', entry)
        devpath = get_device_attribute('ATTRS{devpath}=="(.*?)"', entry)
        path = get_device_attribute('ENV{ID_PATH}=="(.*?)"', entry)

        if name:
            devices[name] = DeviceData(path, vendor, product, serial, devpath)

    return devices


def remove_lines(text: AnyStr, to_remove: AnyStr, ) -> AnyStr:
    """Removes a line from the text based on a pattern.

    Args:
        text: text to modify
        to_remove: regex expression to use as a pattern

    Returns:
        String without all lines containing a match to the pattern.
        If no matches for the pattern were found, the string is returned unaltered
    """
    return re.sub(f'.*{to_remove}.*\n?', '', text)


def remove_rule_by_serial(file_content: AnyStr, serial: AnyStr) -> AnyStr:
    """Removes all rules from the udev file associated with a specific serial number.

    Args:
        file_content: file content of the udev configuration file
        serial: serial number of the entries that should be removed

    Returns:
        udev file content with any rules that contain the specified serial number removed.
        If no matches were found, the string is returned unaltered
    """
    return remove_lines(file_content, f'(?:ATTRS{{serial}}|ENV{{ID_SERIAL}})=="{serial}"')


def remove_rule_by_path(file_content: AnyStr, path: AnyStr) -> AnyStr:
    """Removes all rules from the udev file associated with a specific path.
    Accepts ID_PATH (ENV) and devpath (ATTRS) values.

    Args:
        file_content: file content of the udev configuration file
        path: ID_PATH or devpath of the entries that should be removed

    Returns:
        udev file content with any rules that contain the specified path.
        If no matches were found, the string is returned unaltered.
    """
    return remove_lines(file_content, f'(?:ENV{{ID_PATH}}|ATTRS{{devpath}})=="{path}"')


def remove_rule_by_name(file_content: AnyStr, name: AnyStr) -> AnyStr:
    """Removes all rules form the udev file associated with a specific name (symlink name).

    Args:
        file_content: file content of the udev configuration file
        name: name (symlink) of the entries that should be removed

    Returns:
        udev file content with any rules that contain the specified name.
        If no matches were found, the string is returned unaltered.
    """
    path = [a+b for a, b in re.findall(f'(?:ENV{{ID_PATH}}|ATTRS{{devpath}})=="(.*?)".*SYMLINK\+="{name}"|SYMLINK\+="{name}".*(?:ENV{{ID_PATH}}|ATTRS{{devpath}})=="(.*?)"', file_content)]
    if len(path) > 0:
        return remove_lines(file_content, f'(?:ENV{{ID_PATH}}|ATTRS{{devpath}})=="{path[0]}"')

    serial = [a+b for a, b in re.findall(f'(?:ATTRS{{serial}}|ENV{{ID_SERIAL}})=="(.*?)".*SYMLINK\+="{name}"|SYMLINK\+="{name}".*(?:ATTRS{{serial}}|ENV{{ID_SERIAL}})=="(.*?)"', file_content)]
    if len(serial) > 0:
        return remove_lines(file_content, f'(?:ATTRS{{serial}}|ENV{{ID_SERIAL}})=="{serial[0]}"')

    return file_content


def add_rule(file_content: AnyStr, rule: AnyStr, ) -> AnyStr:
    """Adds the rule to the udev file

    Args:
        file_content: file content of the udev configuration file
        rule: string of the new rule

    Returns:
        udev file content with the new rule appended
    """
    if not rule.endswith("\n"):
        rule += "\n"
    file_content += rule
    return file_content
