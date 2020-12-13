import os
from collections import Counter
from django.core import serializers
from django.db.models import F
from django.db.models.query import QuerySet
from django.utils import timezone as tz
from math import floor

from app.enums import ItemCategoryEnum
from app.models import Donor, Donation, Item
from app.utils.mail import Mail
from app.worker.app_celery import update_percent
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
        self.reboot_stats = {}
        self.qs = queryset
        self.total = total_count + 1  # Add one to wait for mailer
        self.m = Mailer()
        self.reboot_logo_img = open(
            self.static_file_path('img/reboot-black.png'), 'rb').read()
        self.twitter_img = open(
            self.static_file_path('img/twitter.png'), 'rb').read()
        self.facebook_img = open(
            self.static_file_path('img/facebook.png'), 'rb').read()
        self.linkedin_img = open(
            self.static_file_path('img/linkedin.png'), 'rb').read()
        self.yelp_img = open(
            self.static_file_path('img/yelp.png'), 'rb').read()
        self.google_maps_img = open(
            self.static_file_path('img/googlemaps.png'), 'rb').read()
        super().__init__()

    def __call__(self):
        update_percent(0)
        self.m.start_server()

        for row in serializers.deserialize('json', self.qs):
            donation = row.object
            self.donation_pks.append(donation.pk)
            context = self.generate_context(donation)

            pdf = render_to_pdf('pdf/receipt.html', donation.pk, context)
            file_name = f'Tax Receipt {donation.pk}.pdf'
            self.pdfs.append(pdf)
            self.pdf_names.append(file_name)
            self.mails.append(
                self.generate_mail(donation.donor, pdf, file_name))

            self.current_row += 1
            self.log_status_if_pct_update()

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
            self.m.close_server()
            update_percent(100)

    def generate_mail(self, d: Donor, receipt, receipt_name):
        mail_subject = 'reBOOT Canada Donation Receipt'
        mail_raw_body = (
            'Dear Donor,\n'
            'Your donation represents leadership in environmental stewardship and a commitment to providing low-cost access to computers and the internet to members of our community, helping them go to school, look for employment and stay connected. This year, reBOOT Canada will need over 3,000 laptop and desktop computers for use in projects across the country. These units, no longer suitable for corporate applications but otherwise functional or near-functional, form the basis for funding and operating our programs:\n'
            ' • reSTART: basic personal computers with licensed software for at risk youth, seniors and newly settled residents\n'
            ' • reLAY: free 24/7 Wi-Fi in Toronto\'s Parkdale neighbourhood, serving a vulnerable community in downtown Toronto with high concentration of unemployment, shelter risk and mental health support needs\n'
            ' • Skill Development and Leadership training: providing applied work experience through co-op and internship opportunities for youth with barriers to access to employment\n'
            ' • Indigenouse Youth Tool Kit: Providing training, equipment and ongoing support to aboriginal young women and men interested in personal computers and infromation technology\n'
            'We are reaching out to members of the business community in every sector to explore opportunities to support this objectie through the donation of their end of life IT equipments. Your introduction or referral to colleagues in finance, purchasing or IT within your community of suppliers and clients for the purposes of discussing end of life IT assets and refresh cycles would be an enormous help in providing access to tools and infrastructure essential to quality of life and fair access to opporunities for our most vulernable neighbours.\n'
            'Thanks for taking the time to read this note and your generous donation! Please share freely with your colleagues and please take a moment to watch this short video about our recent reBOOT Canada Boot Camp.\n'
            'FRANCISCO ROTA\n'
            'Executive Director\n'
            'Note: This is an automated email. Please send us an email at donation@rebootcanada.ca or call 416 534 6017 x1 for contact.'
        )
        mail_body = (
            '<p>Dear Donor,</p>'
            '<p>Your donation represents leadership in environmental stewardship and a commitment to providing low-cost access to computers and the internet to members of our community, helping them go to school, look for employment and stay connected. This year, reBOOT Canada will need over 3,000 laptop and desktop computers for use in projects across the country. These units, no longer suitable for corporate applications but otherwise functional or near-functional, form the basis for funding and operating our programs:</p>'
            '<ul>'
            '  <li>reSTART: basic personal computers with licensed software for at risk youth, seniors and newly settled residents</li>'
            '  <li>reLAY: free 24/7 Wi-Fi in Toronto\'s Parkdale neighbourhood, serving a vulnerable community in downtown Toronto with high concentration of unemployment, shelter risk and mental health support needs</li>'
            '  <li>Skill Development and Leadership training: providing applied work experience through co-op and internship opportunities for youth with barriers to access to employment</li>'
            '  <li>Indigenouse Youth Tool Kit: Providing training, equipment and ongoing support to aboriginal young women and men interested in personal computers and infromation technology</li>'
            '</ul>'
            '<p>We are reaching out to members of the business community in every sector to explore opportunities to support this objectie through the donation of their end of life IT equipments. Your introduction or referral to colleagues in finance, purchasing or IT within your community of suppliers and clients for the purposes of discussing end of life IT assets and refresh cycles would be an enormous help in providing access to tools and infrastructure essential to quality of life and fair access to opporunities for our most vulernable neighbours.</p>'
            '<p>Thanks for taking the time to read this note and your generous donation! Please share freely with your colleagues and please take a moment to watch <a href="https://www.youtube.com/watch?v=xzwRinp_Rf4">this short video</a> about our recent reBOOT Canada Boot Camp.</p>'
            '<p><b>FRANCISCO ROTA</b></p>'
            '<p><small>Executive Director</small></p>'
            '<table>'
            '  <tr>'
            '    <td>'
            '      <p><img src="cid:reboot-logo" alt="reBOOT Logo"/></p>'
            '      <a href="https://twitter.com/rebootcanada"><img src="cid:twitter" alt="Twitter" /></a>&nbsp;'
            '      <a href="https://www.facebook.com/reBOOTCanada/"><img src="cid:facebook" alt="Facebook" /></a>&nbsp;'
            '      <a href="https://ca.linkedin.com/company/reboot-canada"><img src="cid:linkedin" alt="LinkedIn" /></a>&nbsp;'
            '      <a href="https://www.yelp.ca/biz/reboot-canada-toronto"><img src="cid:yelp" alt="Yelp" /></a>&nbsp;'
            '      <a href="https://goo.gl/u68k6X"><img src="cid:google-maps" alt="Google Maps" /></a>&nbsp;'
            '    </td>'
            '    <td style="vertical-align:top">'
            '      <span><small><b>reBOOT Canada</b></small></span><br/>'
            '      <span><small>103-550 Bayview Avenue</small></span><br/>'
            '      <span><small>Toronto, ON M4W 3X8</small></span><br/>'
            '      <span><small>(416) 534-6017 x2</small></span><br/>'
            '      <span><small>(647) 271-6023</small></span><br/>'
            '      <span><small><a href="https://www.rebootcanada.ca/">rebootcanada.ca</a></small></span>'
            '    </td>'
            '  </tr>'
            '</table>'
            '<p><small>This is an automated email. To schedule your next donation pick-up: email pickup@rebootcanada.ca, call (416) 534-6017 x1, or visit <a href="http://www.rebootcanada.ca/donate.html">rebootcanada.ca/donate</a> today.</small></p>'
        )
        m = Mail(d.email, mail_subject, mail_raw_body, 'alternative')
        m.set_attachment(receipt_name, receipt.getvalue())
        m.add_html_body(mail_body)
        m.add_embbed_image('<reboot-logo>', self.reboot_logo_img)
        m.add_embbed_image('<twitter>', self.twitter_img)
        m.add_embbed_image('<facebook>', self.facebook_img)
        m.add_embbed_image('<linkedin>', self.linkedin_img)
        m.add_embbed_image('<yelp>', self.yelp_img)
        m.add_embbed_image('<google-maps>', self.google_maps_img)
        return m

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
