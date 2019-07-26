from enum import Enum


class ItemCategoryEnum(Enum):
    BATTERY = "battery"
    STORAGE = "storage"
    PERIPHERAL = "peripheral"
    POWER_SUPPLY = "power supply"
    COMPUTER = "computer"
    VIDEO = "video"
    CABLE = "cable"
    NETWORK = "network"
    TABLET = "tablet"
    DISPOSE = "dispose"
    SMALL_ELECTRIC_NON_IT = "small electric non-IT"
    CAMERA = "camera"
    RECYLE = "recyle"
    PRINTER = "printer"
    ASSORTED = "assorted"
    COMPONENT = "component"
    PHONE = "phone"
    CASH = "cash"
    MONITOR = "monitor"
    AUDIO = "audio"
    SOFTWARE = "software"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
