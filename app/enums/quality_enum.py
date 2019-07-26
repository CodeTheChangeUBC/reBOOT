from enum import Enum

class QualityEnum(Enum):
    H = "High"
    M = "Medium"
    L = "Low"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
