import operator as ops
from dateutil.parser import parse

from .base_csv_importer import BaseCsvImporter
from app.models import Donor, Donation


class WebformDataImporter(BaseCsvImporter):
    """Takes rebootcanada.ca/donation-form formatted file path and imports into
    the database format into appropriate tables.

    :param str csvfile: csvfile path
    """

    # bulk_model = Donation

    def parse_row(self, row):
        donor = self._goc_donor(self._parse_donor(row))
        self._create_donation(self._parse_donation(row), donor)
        # self.model_bulk.append(
        #     self._new_donation(self._parse_donation(row), donor))

    def _parse_donor(self, row):
        """Takes a csv row and parses relevant Donor data

        :param OrderedDict row: csv row
        :return: Donor data dict
        :rtype: dict
        """
        want_receipt = row["Tax Receipt Required"].lower()
        want_receipt = "REFUSED" if want_receipt == "no" else "EMAIL"
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
            "telephone_number": "",
            "mobile_number": row["Phone Number"],
            "address_line_one": row["Address (Street Address)"],
            "address_line_two": row["Address (Address Line 2)"],
            "city": row["Address (City)"],
            "province": row["Address (State / Province)"],
            "postal_code": row["Address (ZIP / Postal Code)"].upper(),
            # "customer_ref": "",
            "documented_at": self._parse_date(row["Entry Date"]),
        }

    def _parse_donation(self, row):
        note = row["Notes: (parking, buzzer, dock availability, stairs, etc.)"]
        links = row["Images or Inventory List"]
        certificate = row["Do you require a certificate of data erasure?"]
        certificate = "Yes" if certificate.lower() == "yes" else "No"
        received_by = row["1"]
        items = "\n".join(self._parse_items(row))

        return {
            "pledge_date": parse(row["Entry Date"]).date(),
            "pick_up": row["Address (ZIP / Postal Code)"].upper(),
            "source": "WEBSITE_IMPORT",  # fixed
            "documented_at": self._parse_date(row["Entry Date"]),
            "notes": (
                f"Received By: {received_by}\n",
                f"Links: {links}\n",
                f"Require Certificate of Data Erasure?: {certificate}\n",
                f"Items: {items}\n",
                f"Additional Notes: {note}",
            ),
        }

    def _parse_items(self, row):
        items = [colval.strip() for (colkey, colval) in row.items()
                 if "Donation Items" in colkey]
        return filter(ops.truth, items)

    def _goc_donor(self, data):
        """get_or_create a Donor
        :param dict data: A Donor data dict
        :return: Donor object got_or_created from the data
        :rtype: app.models.Donor
        """
        try:
            if "anonymous" in data.get("contact_name").lower():
                d = Donor.objects.create(
                    donor_name="Anonymous",
                    contact_name="Anonymous",
                    email="",
                    mobile_number="")
            else:
                d = Donor.objects.get(
                    contact_name=data.get("contact_name"),
                    email=data.get("email"),
                    mobile_number=data.get("mobile_number"))
        except Exception:
            d = Donor.objects.create(**data)
        return d

    def _create_donation(self, data, donor):
        """Create a new Donation object

        :param dict data: A Donation data dict
        :param app.models.Donor donor: A Donor object
        :return: Donation object from data
        :rtype: app.models.Donation: Donation object
        """
        return Donation.objects.create(donor=donor, **data)

    @staticmethod
    def _parse_date(date_f):
        """ Takes dynamic date formats and unifies them into Y-m-d format
        """
        date = parse(date_f)
        return date.strftime('%Y-%m-%d')
