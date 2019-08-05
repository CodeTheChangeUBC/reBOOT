from .resource_enum import ResourceEnum


class DonationStatusEnum(ResourceEnum):
    OPENED = "Opened"
    IN_TEST = "In Test"
    EVALED = "Evaled"
    RECEIPTED = "Receipted"

    @classmethod
    def default(cls):
        return "OPENED"
