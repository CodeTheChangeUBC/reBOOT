UNCHANGEABLE_ERROR = 'This instance may not be modified further since the related tax receipt was generated.'
PERMISSION_DENIED = 'Permission denied. Please contact admin for access.'

BASE_DONATION = 'are not valid for tax receipt generation. Please review and try again.'
UNVERIFIED_DONATION = f'Unverified donations {BASE_DONATION}'
UNEVALUATED_DONATION = f'Donations with not evaluated items {BASE_DONATION}'
RECEIPTED_DONATION = f'Previously receipted donations {BASE_DONATION}'
EMPTY_DONATION = f'Donations with no items {BASE_DONATION}'
DONATION_EVENT_ORDER_ERROR = 'Donation events must occur in this order: pledged, received, tested, valuated, and receipted. Please set previous event dates.'
