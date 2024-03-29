ALL = [
    "add_logentry",
    "change_logentry",
    "delete_logentry",
    "view_logentry",
    "can_export_data",
    "can_import_historical",
    "can_import_third_party",
    "can_import_website",
    "add_donation",
    "change_donation",
    "delete_donation",
    "destroy_donation",
    "generate_tax_receipt",
    "view_donation",
    "add_donor",
    "change_donor",
    "delete_donor",
    "destroy_donor",
    "view_donor",
    "add_item",
    "change_item",
    "delete_item",
    "destroy_item",
    "update_status_item",
    "update_value_item",
    "view_item",
    "add_itemdevice",
    "change_itemdevice",
    "delete_itemdevice",
    "view_itemdevice",
    "add_itemdevicetype",
    "change_itemdevicetype",
    "delete_itemdevicetype",
    "view_itemdevicetype",
    "add_group",
    "change_group",
    "delete_group",
    "view_group",
    "add_permission",
    "change_permission",
    "delete_permission",
    "view_permission",
    "add_user",
    "change_user",
    "delete_user",
    "view_user",
    "add_contenttype",
    "change_contenttype",
    "delete_contenttype",
    "view_contenttype",
    "add_session",
    "change_session",
    "delete_session",
    "view_session",
]

FRONTLINE = [
    'add_donation',
    'change_donation',
    'delete_donation',
    'view_donation',
    'add_donor',
    'change_donor',
    'delete_donor',
    'view_donor',
    'add_item',
    'change_item',
    'delete_item',
    'view_item',
    'add_itemdevice',
    'change_itemdevice',
    'delete_itemdevice',
    'add_itemdevicetype',
    'change_itemdevicetype',
    'delete_itemdevicetype',
]

MANAGEMENT = FRONTLINE + [
    'can_import_historical',
    'can_import_third_party',
    'can_import_website',
    'can_export_data',
    'generate_tax_receipt',
    'update_status_item',
    'update_value_item',
    'generate_tax_receipt',
]
