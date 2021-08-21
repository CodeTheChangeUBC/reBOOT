import os
from collections import Counter
from django.core import serializers
from django.db.models import F
from django.db.models.query import QuerySet
from django.utils import timezone as tz
from math import floor

from app.enums import ItemCategoryEnum
from app.models import Donor, Donation, Item
from app.worker.app_celery import update_percent
from app.utils.donation_mail_generator import DonationMailGenerator
from app.utils.mailer import Mailer
from app.worker.tasks.logger_task import LoggerTask
from app.utils.files import render_to_pdf, generate_zip


class Receiptor(LoggerTask):
    reboot_stat = None              # Current year's reboot-wide stat
    donation_pks = None             # List of donations to marked as receipted
    pdfs, pdf_names = None, None    # Generated pdfs files and file names
    mails = None                    # Mails to be sent
    reboot_stats = None             # Cache of yearly reboot stats
    current_row, current_pct = 0, 0

    def __init__(self, queryset: QuerySet, total_count: int):
        self.donation_pks = []
        self.pdfs, self.pdf_names = [], []
        self.mails = []
        self.shouldSendCopy = False
        self.reboot_stats = {}
        self.qs = queryset
        self.total = total_count + 1  # Add one to wait for mailer
        self.m = Mailer()
        self.generate_mail = DonationMailGenerator()
        super().__init__()

    def __call__(self):
        update_percent(0)
        # Note: SMTP may fail due to Gmail security policy. Check credentials
        # and settings
        if self.shouldSendCopy:
            self.m.start_server()

        for row in serializers.deserialize('json', self.qs):
            donation = row.object
            self.donation_pks.append(donation.pk)
            context = self.generate_context(donation)

            pdf = render_to_pdf('pdf/receipt.html', donation, context)
            file_name = f'{donation.pk} {donation.donor.donor_name}.pdf'
            self.pdfs.append(pdf)
            self.pdf_names.append(file_name)
            self.mails.append(
                self.generate_mail(donation.donor, pdf, file_name))

            self.current_row += 1
            self.log_status_if_pct_update()

        if self.shouldSendCopy:
            self.logger.info('Receipt generation completed; Sending Mails')
            self.m.send_mails(self.mails)
            self.logger.info(f'Sent {len(self.mails)} mails')

        self.logger.info(f"Receipted {self.current_row} donation(s)")
        Donation.objects.filter(pk__in=self.donation_pks).update(
            tax_receipt_created_at=tz.localtime())

        try:
            if len(self.pdfs) == 1:
                return self.pdfs[0]
            else:
                return generate_zip(self.pdfs, self.pdf_names)
        finally:
            if self.shouldSendCopy:
                self.m.close_server()
            update_percent(100)

    def generate_context(self, d: Donation):
        total_qty, total_value = d.total_quantity_and_value()
        today_date = tz.localdate().strftime('%b %d, %Y')
        number_of_padding_needed = max(10 - d.item_set.count(), 0)

        return {
            'reboot_stat': self.get_full_year_stat(d.donate_date.year),
            'donor_stat': self.reboot_yearly_stat(d.donate_date.year, d.donor),
            'logo_path': self.static_file_path('img/reboot-round.png'),
            'sign_path': self.static_file_path('img/colin-webster.png'),
            'footer_path': self.static_file_path('img/reboot-footer.png'),
            'slogan_path': self.static_file_path('img/reboot-slogan.png'),
            'css_path': self.static_file_path('css/receipt.css'),
            'generated_date': today_date,
            'date': d.donate_date,
            'donor': d.donor,
            'tax_receipt_no': d.pk,
            'list_of_items': d.item_set.all(),
            'total_value': format(total_value, '.2f'),
            'total_qty': total_qty,
            'pick_up': d.pick_up,
            'empty_rows': [i for i in range(number_of_padding_needed)]
        }

    def get_full_year_stat(self, year: int):
        if year not in self.reboot_stats:
            self.reboot_stats[year] = self.reboot_yearly_stat(year)
        return self.reboot_stats[year]

    def log_status_if_pct_update(self):
        """ Calculates new counts and percentages and logs if diff pct
        """
        new_pct = floor(100 * float(self.current_row) / float(self.total))
        if new_pct != self.current_pct:
            self.current_pct = new_pct
            update_percent(new_pct)
            self.logger.info(
                f"Processed row #{self.current_row} ||| {new_pct}%")

    @staticmethod
    def static_file_path(file_name: str):
        return os.path.join(os.getcwd(), 'static/admin', file_name)

    @staticmethod
    def reboot_yearly_stat(year: int, donor: Donor = None):
        qs = Item.objects.filter(donation__pk__startswith=year)
        if donor:
            qs = qs.filter(donation__donor=donor)
        qs = qs.values(
            'quantity', category=F('device__dtype__category'))
        raw_summary = qs.order_by('quantity').values_list(
            'category', 'quantity')

        summary = Counter()
        for category, quantity in raw_summary:
            summary[category] += quantity

        counts = sum(summary.values())
        computers = summary.get(ItemCategoryEnum.COMPUTER.name, 0)
        printers = summary.get(ItemCategoryEnum.PRINTER.name, 0)
        monitors = summary.get(ItemCategoryEnum.MONITOR.name, 0)
        storages = summary.get(ItemCategoryEnum.STORAGE.name, 0)
        others = counts - computers - printers - monitors - storages

        return {
            'computers': computers,
            'printers': printers,
            'monitors': monitors,
            'storage': storages,
            'others': others,
        }
