from django.utils import timezone as tz

from .base_csv_importer import BaseCsvImporter
from app.constants.item_map import ITEM_MAP
from app.enums import DonationStatusEnum, ItemStatusEnum
from app.models import Donor, Donation, Item, ItemDevice, ItemDeviceType

class HistoricalDataImporter(BaseCsvImporter):
    """ Takes 10b format file path and imports into the database using the 10x
    format into the appropriate tables

    :param str csvfile: csvfile path
    """
    bulk_model = Item

    def parse_row(self, row):
        donor = self._goc_donor(self._parse_donor(row))
        donation = self._goc_donation(self._parse_donation(row), donor)
        device_type = self._goc_device_type(self._parse_device_type(row))
        device = self._goc_item_device(
            self._parse_item_device(row), device_type)
        self.model_bulk.append(
            self._new_item(self._parse_item(row), donation, device))

    def _parse_donor(self, row):
        """ Takes a row and parses relevant Donor data into a dict

        :param dict row: A CSV row dict
        :return: Donor related data dict
        :rtype: dict
        """
        receipt_option_f = {
            "Not Needed": "REFUSED",
            "E-Mail": "EMAIL",
            "Mail": "MAIL"
        }[row["TRV"]]
        documented_at_f = self._parse_date(row["Date"])
        tele_no_f = row["Telephone"] if row["Telephone"] != "xxxxxxxx" else ""

        return {
            "donor_name": row["Donor Name"],
            "contact_name": row["Contact"],
            "email": row["Email"],
            "want_receipt": receipt_option_f,
            "telephone_number": tele_no_f,
            "mobile_number": row["Mobile"],
            "address_line_one": row["Address"],
            "address_line_two": row["Unit"],
            "city": row["City"],
            "province": row["Prov."],
            "postal_code": row["Postal Code"][:7],
            "customer_ref": row["CustRef"],
            "documented_at": documented_at_f
        }

    def _parse_donation(self, row):
        """ Takes a csv row and parses relevant Donation data into a dict

        :param dict row: A CSV row dict
        :return: Donation related data dict
        :rtype: dict
        """
        donate_date_f = self._parse_date(row["Date"])
        documented_at_f = self._parse_date(row["Date"])

        return {
            "tax_receipt_no": row["TR#"],
            "donate_date": donate_date_f,
            "pledge_date": donate_date_f,
            "pick_up": row["PPC"],
            "status": DonationStatusEnum.RECEIPTED.name,
            "source": "HISTORICAL_DATA",    # Fixed
            "documented_at": documented_at_f,
            "tax_receipt_created_at": tz.now()
        }

    def _parse_device_type(self, row):
        """ Takes a csv row and parses relevant ItemDeviceType data into a dict

        :param dict row: A CSV row dict
        :return: ItemDeviceType related data dict
        :rtype: dict
        """
        return ITEM_MAP[row["Item Description"].lower()]

    def _parse_item_device(self, row):
        """ Takes a csv row and parses relevant ItemDevice data into a dict

        :param dict row: A CSV row dict
        :return: ItemDevice related data dict
        :rtype: dict
        """
        return {
            "make": row["Manufacturer"],
            "model": row["Model"],
            "cpu_type": "",
            "speed": "",
            "memory": None,
            "hd_size": None,
            "screen_size": "",
            "hdd_serial_number": "",
            "operating_system": ""
        }

    def _parse_item(self, row):
        """ Takes a csv row and parses relevant Item data into a dict

        :param dict row: A CSV row dict
        :return: Item related data dict
        :rtype: dict
        """
        working_f = row["Working"].lower() == "y"
        value_f = 0 if not row["Value"] else row["Value"]
        documented_at_f = self._parse_date(row["Date"])
        batch_f = "" if row["Batch"] == "0" else row["Batch"]

        return {
            "serial_number": "",
            "asset_tag": "",
            "particulars": row["Item Particulars"],
            "quantity": row["Qty"],
            "working": working_f,
            "condition": row["Condition"],
            "quality": row["Quality"],
            "batch": batch_f,
            "value": value_f,
            "verified": True,
            "documented_at": documented_at_f,
            "status": ItemStatusEnum.RECEIVED.name,
            "notes": ""
            # "weight":
            # "valuation_date":
            # "valuation_supporting_doc":
        }

    def _goc_donor(self, data):
        """ get_or_create a Donor

        :param dict row: A Donor dict
        :return: Donor object
        :rtype: app.models.Donor instance
        """
        donor, unique = Donor.objects.get_or_create(**data)
        return donor


    def _goc_donation(self, data, donor):
        """ get_or_create a Donation

        :param dict row: A Donation dict
        :param obj donor: app.model.Donor object
        :return: Donation object
        :rtype: app.models.Donation instance
        """
        try:
            d = Donation.objects.get(tax_receipt_no=data.get("tax_receipt_no"))
        except Exception:
            d = Donation.objects.create(donor=donor, **data)
        return d


    def _goc_device_type(self, data):
        """ get_or_create a ItemDeviceType

        :param dict row: A ItemDeviceType dict
        :return: ItemDeviceType object
        :rtype: app.models.ItemDeviceType instance
        """
        dtype, unique = ItemDeviceType.objects.get_or_create(**data)
        return dtype


    def _goc_item_device(self, data, dtype):
        """ get_or_create a ItemDevice

        :param dict row: A ItemDevice dict
        :param obj device_type: app.model.ItemDeviceType object
        :return: ItemDevice object
        :rtype: app.models.ItemDevice instance
        """
        i, unique = ItemDevice.objects.get_or_create(dtype=dtype, **data)
        return i




    def _new_item(self, data, donation, device):
        """ Initialize a new Item object

        :param dict row: A Item dict
        :param obj donation: app.model.Donation object
        :param obj device: app.model.ItemDevice object
        :return: Item object
        :rtype: app.models.Item instance
        """
        return Item(donation=donation, device=device, **data)
