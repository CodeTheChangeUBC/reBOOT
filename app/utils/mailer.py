import smtplib
from decouple import config

from app.utils.mail import Mail


class Mailer(object):
    '''
    Static mailer server class
    '''
    def __init__(self, *args, **kwargs):
        self.host = kwargs.get('host', config('EMAIL_HOST'))
        self.from_display = kwargs.get(
            'from_display', config('EMAIL_HOST_DISPLAY_NAME', 'reBOOT Canada'))
        self.from_email = kwargs.get('from_email', config('EMAIL_HOST_USER'))
        self.from_password = kwargs.get(
            'from_password', config('EMAIL_HOST_PASSWORD'))

    def start_server(self):
        self.s = smtplib.SMTP(self.host, 587)
        self.s.ehlo()
        self.s.starttls()
        self.s.login(self.from_email, self.from_password)

    def display_sender(self):
        return f'{self.from_display} <{self.from_email}>'

    def send_mails(self, mails: [Mail]):
        for m in mails:
            self.send_mail(m)

    def send_mail(self, mail: Mail):
        if mail.get_from() is None:
            mail.set_from(self.display_sender())
        self.s.sendmail(mail.get_from(), mail.get_to(), mail.as_string())

    def close_server(self):
        self.s.close()
