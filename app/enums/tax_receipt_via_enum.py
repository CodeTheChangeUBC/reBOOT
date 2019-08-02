from .resource_enum import ResourceEnum


class TaxReceiptViaEnum(ResourceEnum):
    EMAIL = "Email"
    MAIL = "Mail"
    REFUSED = "Refused"

    @classmethod
    def default(cls):
        return "EMAIL"
