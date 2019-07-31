from .resource_enum import ResourceEnum

class SourceEnum(ResourceEnum):
    DIRECT_MANUAL_INPUT = "Direct Manual Input"
    ONLINE_FORM = "On-line Form"
    WEBSITE_IMPORT = "Website File Import"
    HISTORICAL_DATA = "Historical Data"
    THIRD_PARTY_DATA = "3rd Party Data"
