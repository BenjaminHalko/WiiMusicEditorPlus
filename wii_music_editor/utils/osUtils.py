import platform
from enum import Enum


class SystemType(Enum):
    Windows = 0,
    Mac = 1,
    Linux = 2


def choose_from_os(array: list):
    if currentSystem == SystemType.Windows:
        return array[0]
    elif currentSystem == SystemType.Mac:
        return array[1]
    else:
        return array[2]


currentSystem: SystemType = SystemType.Linux
if platform.system() == "Windows":
    currentSystem = SystemType.Windows
elif platform.system() == "Darwin":
    currentSystem = SystemType.Mac
