from dataclasses import dataclass
from typing import Optional, AnyStr


@dataclass
class DeviceData:
    """Class for keeping track of device information"""
    path: Optional[AnyStr]
    vendor_id: Optional[AnyStr]
    model_id: Optional[AnyStr]
    serial: Optional[AnyStr]
    devpath: Optional[AnyStr]
