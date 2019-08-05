from enum import Enum


class ResourceEnum(Enum):
    '''Note about Enum:
    First constant listed will be used as the default options if default is True
    '''
    @classmethod
    def choices(cls):
        '''
        Return a tuple of variable names and values for django model choices
        '''
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def lookup(cls, value):
        '''
        Return the variable name given value from enum set
        '''
        for i in cls:
            if i.value == value:
                return i.name
        raise LookupError

    @classmethod
    def default(cls):
        '''
        Returns the default option to use from enum.
        Must be implemented by the subclass. Use the variable name as return val
        '''
        raise NotImplementedError
