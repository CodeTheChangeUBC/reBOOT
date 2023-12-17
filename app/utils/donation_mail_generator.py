import os

from app.models import Donor
from app.utils.mail import Mail


class DonationMailGenerator():
    '''
    Generator class for generating Donation thank-you mails. Consumes tax
    receipt pdfs and returns Mail.
    '''
    subject = 'reBOOT Canada Donation Receipt'

    def __init__(self):
        with open(self.getfp('txt/donation_email_raw_body.txt'), 'rb') as f:
            self.raw_body = f.read()
        with open(self.getfp('html/donation_email_body.html'), 'rb') as f:
            self.body = f.read()
        with open(self.getfp('img/reboot-black.png'), 'rb') as f:
            self.reboot_img = f.read()
        with open(self.getfp('img/twitter.png'), 'rb') as f:
            self.twitter_img = f.read()
        with open(self.getfp('img/facebook.png'), 'rb') as f:
            self.facebook_img = f.read()
        with open(self.getfp('img/linkedin.png'), 'rb') as f:
            self.linkedin_img = f.read()
        with open(self.getfp('img/yelp.png'), 'rb') as f:
            self.yelp_img = f.read()
        with open(self.getfp('img/googlemaps.png'), 'rb') as f:
            self.gmaps_img = f.read()

    def __call__(self, d: Donor, receipt, receipt_name):
        m = Mail(
            "donation@rebootcanada.ca",
            self.subject,
            self.raw_body,
            'alternative')
        m.add_html_body(self.body)
        m.set_attachment(receipt_name, receipt.getvalue())
        m.add_embbed_image('<reboot-logo>', self.reboot_img)
        m.add_embbed_image('<twitter>', self.twitter_img)
        m.add_embbed_image('<facebook>', self.facebook_img)
        m.add_embbed_image('<linkedin>', self.linkedin_img)
        m.add_embbed_image('<yelp>', self.yelp_img)
        m.add_embbed_image('<google-maps>', self.gmaps_img)
        return m

    @staticmethod
    def getfp(file_name: str):
        return os.path.join(os.getcwd(), 'static/admin', file_name)
