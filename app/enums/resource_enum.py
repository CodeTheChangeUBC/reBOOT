from enum import Enum


class ResourceEnum(Enum):
    @classmethod
    def choices(cls):
        '''
        Return a tuple of variable names and values for django model choices
        '''
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def default(cls):
        '''
        Returns the default option to use from enum.
        Must be implemented by subclass. Use the variable name as return val
        '''
        raise NotImplementedError
