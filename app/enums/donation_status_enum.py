from .resource_enum import ResourceEnum


class DonationStatusEnum(ResourceEnum):
    OPENED = "Opened"
    RECEIVED = "Received"
    TESTED = "Tested"
    EVALED = "Evaled"
    RECEIPTED = "Receipted"

    @classmethod
    def default(cls):
        return "OPENED"
