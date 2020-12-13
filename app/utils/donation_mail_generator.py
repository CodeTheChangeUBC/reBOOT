import os

from app.models import Donor
from app.utils.mail import Mail


class DonationMailGenerator():
    '''
    Generator class for generating Donation thank-you mails. Consumes tax
    receipt pdfs and returns Mail.
    '''
    subject = 'reBOOT Canada Donation Receipt'
    raw_body = (
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
    body = (
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

    def __init__(self):
        self.reboot_img = open(self.getfp('img/reboot-black.png'), 'rb').read()
        self.twitter_img = open(self.getfp('img/twitter.png'), 'rb').read()
        self.facebook_img = open(self.getfp('img/facebook.png'), 'rb').read()
        self.linkedin_img = open(self.getfp('img/linkedin.png'), 'rb').read()
        self.yelp_img = open(self.getfp('img/yelp.png'), 'rb').read()
        self.gmaps_img = open(self.getfp('img/googlemaps.png'), 'rb').read()

    def __call__(self, d: Donor, receipt, receipt_name):
        m = Mail(d.email, self.subject, self.raw_body, 'alternative')
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
