import operator as ops
from dateutil.parser import parse

from .base_csv_importer import BaseCsvImporter
from app.models import Donor, Donation


class WebformDataImporter(BaseCsvImporter):
    """Takes rebootcanada.ca/donation-form formatted file path and imports into
    the database format into appropriate tables.

    :param str csvfile: csvfile path
    """

    bulk_model = Donation

    def parse_row(self, row):
        donor = self._goc_donor(self._parse_donor(row))
        self.model_bulk.append(
            self._new_donation(self._parse_donation(row), donor))

    def _parse_donor(self, row):
        """Takes a csv row and parses relevant Donor data

        :param OrderedDict row: csv row
        :return: Donor data dict
        :rtype: dict
        """
        want_receipt = {
            "yes": "EMAIL",
            "no": "REFUSED",
        }.get(row["Tax Receipt Required"].lower(), "EMAIL")
        donor_name = row["Business Name (if applicable)"]
        contact_name = " ".join(filter(ops.truth, [
            row["Contact Name (First)"],
            row["Contact Name (Middle)"],
            row["Contact Name (Last)"]
        ]))
        donor_name = donor_name if donor_name else contact_name

        return {
            "donor_name": donor_name,
            "contact_name": contact_name,
            "email": row["Email Address"],
            "want_receipt": want_receipt,
            "telephone_number": row["Phone Number"],
            "mobile_number": "",
            "address_line_one": row["Address (Street Address)"],
            "address_line_two": row["Address (Address Line 2)"],
            "city": row["Address (City)"],
            "province": row["Address (State / Province)"],
            "postal_code": row["Address (ZIP / Postal Code)"],
            # "customer_ref": "",
            "documented_at": self._parse_date(row["Entry Date"]),
        }

    def _parse_donation(self, row):
        return {
            "pledge_date": parse(row["Entry Date"]).date(),
            # "pick_up": row[""],  # ?
            "source": "WEBSITE_IMPORT",  # fixed
            "documented_at": self._parse_date(row["Entry Date"]),
            # "notes": "",
        }
        pass

    def _goc_donor(self, data):
        """get_or_create a Donor
: param dict data: A Donor data dict: return: Donor object got_or_created from the data        : rtype: app.models.Donor:         """
        donor, unique = Donor.objects.get_or_create(**data) return donor

    def _new_donation(self, data, donor):
        """Initialize a new Donation object
: param dict data: A Donation data dict: param app.models.Donor donor: A Donor object: return: Donation object from data to be bulk created
        : rtype app.models.Donation: Donation object
        """
        try:
            d = Donation(donor=donor, **data)
            d.clean_fields()
        except Exception as e:
            self.logger.error(f"Donation data: {d.underscore_serialize()}")
            raise e
        return d

    @staticmethod
    def _parse_date(date_f):
        """ Takes dynamic date formats and unifies them into Y-m-d format
        """
        date = parse(date_f)
        return date.strftime('%Y-%m-%d')
