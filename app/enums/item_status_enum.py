from .resource_enum import ResourceEnum


class ItemStatusEnum(ResourceEnum):
    PLEDGED = "Pledged"
    RECEIVED = "Received"
    TESTED = "Tested"
    REFURBISHED = "Refurbished"
    SOLD = "Sold"
    RECYCLED = "Recycled"

    @classmethod
    def default(cls):
        return "PLEDGED"
