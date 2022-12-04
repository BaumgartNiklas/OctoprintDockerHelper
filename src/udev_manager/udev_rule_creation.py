from typing import AnyStr


def create_rule_attribute(parameter_name: AnyStr, parameter_value: AnyStr) -> AnyStr:
    """
    Creates an Attribute comparison for an udev rule.

    Args:
        parameter_name: Name of the attribute
        parameter_value: value of the attribute

    Returns:
    string for an udev rule comparing the attribute to the specified value
    """
    attribute = f"ATTRS{{{parameter_name}}}==\"{parameter_value}\""
    return attribute


def create_rule_env(parameter_name: AnyStr, parameter_value: AnyStr) -> AnyStr:
    """
    Creates an Environment Attribute comparison for an udev rule.

    Args:
        parameter_name: Name of the environment variable
        parameter_value: value of the environment variable

    Returns:
        string for udev rule comparing the environment variable to the specified value
    """
    return f'ENV{{{parameter_name}}}=="{parameter_value}"'


def create_startstop_udev_rule(name: AnyStr, start_command: AnyStr, stop_command: AnyStr, serial: AnyStr = None, path: AnyStr = None, vendor_id: AnyStr = None, model_id: AnyStr = None) -> AnyStr:
    """
    Creates an udev rule for a serial usb device. The udev rule creates a symlink to the device with the name specified in the name parameter
    On connect and disconnect, the respective command is executed. The commands have to be specified with absolute file paths
    Either the serial number or the path has to be specified.

    Args:
        name: name for the usb device
        start_command: linux command to execute when the device is connected. All file paths have to be absolute
        stop_command: linux command to execute when the device is disconnected. All file paths have to be absolute
        serial: serial number of the device. If not specified, a path has to be specified
        path: usb path of the device. If not specified, a serial number has to be specified
        vendor_id: vendor it of the device
        model_id:  model id of the device

    Returns:
        string of the complete udev rule

    Raises:
        ValueError: If serial and devpath are None
    """
    config_add = f'SUBSYSTEM=="tty", '

    if vendor_id is not None:
        config_add += f'{create_rule_env("ID_VENDOR_ID", vendor_id)}, '
    if model_id is not None:
        config_add += f'{create_rule_env("ID_MODEL_ID", model_id)}, '

    if serial is not None:
        config_add += f'{create_rule_env("ID_SERIAL", serial)}, '
    elif path is not None:
        config_add += f'{create_rule_env("ID_PATH", path)}, '
    else:
        raise ValueError("Either serial or devpath has to be specified")

    config_remove = config_add

    config_add += (f'SYMLINK+="{name}", '
                   f'ACTION=="add", '
                   f'RUN+="{start_command}"')
    config_remove += (f'ACTION=="remove", '
                      f'RUN+="{stop_command}"')

    return f'{config_add}\n{config_remove}'


def create_udev_rule(name: AnyStr, serial: AnyStr = None, devpath: AnyStr = None, path: AnyStr = None, vendor_id: AnyStr = None, product_id: AnyStr = None) -> AnyStr:
    """
    Creates an udev rule for a serial usb device. The udev rule creates a symlink to the device with the name specified in the name parameter
    At least the serial number, devpath or path has to be specified. If more than one is specified, the serial number is preferred (serial > devpath > path)

    Args:
        name: name for the usb device
        serial: serial number of the device.
        devpath: devpath of the device.
        path: id_path of the device.
        vendor_id: vendor it of the device
        product_id: product id of the device

    Returns:
        string of the complete udev rule

    Raises:
        ValueError: If serial and devpath are None
    """
    config = f'SUBSYSTEM=="tty", '

    if vendor_id is not None:
        config += f'{create_rule_attribute("idVendor", vendor_id)}, '
    if product_id is not None:
        config += f'{create_rule_attribute("idProduct", product_id)}, '

    if serial is not None:
        config += f'{create_rule_attribute("serial", serial)}, '
    elif devpath is not None:
        config += f'{create_rule_attribute("devpath", devpath)}, '
    elif path is not None:
        config += f'{create_rule_env("ID_PATH", path)}'
    else:
        raise ValueError("Either serial or devpath or path has to be specified")

    config += f'SYMLINK+="{name}"'

    return config
