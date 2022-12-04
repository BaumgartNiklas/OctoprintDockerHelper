import pyudev
from .device_data import DeviceData


def get_device_list() -> list[DeviceData]:
    """
    Creates a list of information of connected usb devices.
    The included information is the vendor id, model id, serial number, path and devpath.

    Returns:
        List of DeviceData objects
    """
    devices = []

    context = pyudev.Context()
    for device in context.list_devices(subsystem='tty'):
        path = device.get("ID_PATH", None)

        # find better check if device is connected
        if path is None:
            continue

        vendor_id = device.get("ID_VENDOR_ID", None)
        model_id = device.get("ID_MODEL_ID", None)
        serial = device.get("ID_SERIAL", None)

        devpath = device.attributes.get("devpath", None)
        for parent in device.ancestors:
            if devpath is not None:
                devpath = devpath.decode('ascii')
                break

            devpath = parent.attributes.get("devpath", None)

        devices.append(DeviceData(path, vendor_id, model_id, serial, devpath))

    return devices
