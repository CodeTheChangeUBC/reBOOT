from enum import Enum


class ResourceEnum(Enum):
    '''Note about Enum:
    First constant listed will be used as the default options if default is True
    '''
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
