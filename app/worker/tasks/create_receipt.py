import os
from collections import Counter
from django.core import serializers
from django.db.models import F
from django.utils import timezone as tz

from app.enums import ItemCategoryEnum
from app.models import Donation, Item
from app.worker.app_celery import update_percent
from app.worker.tasks.base_task import BaseTask
from app.utils.files import render_to_pdf, generate_zip


class Receiptor(BaseTask):
    reboot_stat = None              # Current year's reboot-wide stat
    donation_pks = None             # List of donations to marked as receipted
    pdfs, pdf_names = None, None    # Generated pdfs files and file names
    current_row, current_pct = 0, 0

    def __init__(self, queryset, total_count):
        self.donation_pks = []
        self.pdfs, self.pdf_names = [], []
        self.reboot_stat = Receiptor.reboot_yearly_stat()

        self.qs = queryset
        self.total = total_count
        super().__init__()

    def __call__(self):
        update_percent(0)
        for row in serializers.deserialize('json', self.qs):
            donation = row.object
            self.donation_pks.append(donation.pk)
            context = self.generate_context(donation)

            response = render_to_pdf('pdf/receipt.html', donation.pk, context)
            self.pdfs.append(response)
            self.pdf_names.append(f'Tax Receipt {donation.pk}.pdf')

            self.current_row += 1
            self.log_status_if_pct_update()

        self.logger.info(f"Receipted {self.current_row} donation(s)")
        Donation.objects.filter(pk__in=self.donation_pks).update(
            tax_receipt_created_at=tz.localtime())

        self.logger.info('Receipt generation completed')
        if len(self.pdfs) == 1:
            return self.pdfs[0]
        else:
            return generate_zip(self.pdfs, self.pdf_names)

    def generate_context(self, donation: Donation):
        total_qty, total_value = donation.total_quantity_and_value()
        today_date = tz.localdate().strftime('%b %d, %Y')
        number_of_padding_needed = max(15 - donation.item_set.count(), 0)

        return {
            'reboot_stat': self.reboot_stat,
            'donor_stat': Receiptor.reboot_yearly_stat(donation.donor),
            'logo_path': Receiptor.static_file_path('img/reboot-logo-2.png'),
            'sign_path': Receiptor.static_file_path('img/colin-webster.png'),
            'footer_path': Receiptor.static_file_path('img/reboot-footer.png'),
            'slogan_path': Receiptor.static_file_path('img/reboot-slogan.png'),
            'css_path': Receiptor.static_file_path('css/receipt.css'),
            'generated_date': today_date,
            'date': donation.donate_date,
            'donor': donation.donor,
            'tax_receipt_no': donation.pk,
            'list_of_items': donation.item_set.all(),
            'total_value': format(total_value, '.2f'),
            'total_qty': total_qty,
            'pick_up': donation.pick_up,
            'empty_rows': [i for i in range(number_of_padding_needed)]
        }

    def log_status_if_pct_update(self):
        """ Calculates new counts and percentages and logs if diff pct
        """
        new_pct = int(100 * float(self.current_row) / float(self.total))
        if new_pct != self.current_pct:
            self.current_pct = new_pct
            update_percent(new_pct)
            self.logger.info(
                f"Processed row #{self.current_row} ||| {new_pct}%")

    @staticmethod
    def static_file_path(file_name):
        return os.path.join(os.getcwd(), 'static/admin', file_name)

    @staticmethod
    def reboot_yearly_stat(donor=None):
        year = tz.localdate().year
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
