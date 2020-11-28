import smtplib
from decouple import config

from app.worker.models.mail import Mail
from app.worker.tasks.logger_task import LoggerTask


class Mailer(LoggerTask):
    def __init__(self, *args, **kwargs):
        self.host = kwargs.get('host', config('EMAIL_HOST'))
        self.from_email = kwargs.get('from_email', config('EMAIL_HOST_USER'))
        self.from_password = kwargs.get(
            'from_password', config('EMAIL_HOST_PASSWORD'))
        super().__init__()

    def start_server(self):
        self.server = smtplib.SMTP(self.host, 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.from_email, self.from_password)

    def send_mails(self, mails: [Mail]):
        sent = 0
        for mail in mails:
            sent += self.send_mail(mail)
        return sent

    def send_mail(self, mail: Mail):
        if mail.msg['From'] is None:
            mail.set_from(self.from_email)
        content = mail.as_string()
        self.server.sendmail(self.from_email, mail.to_email, content)
        return 1

    def close(self):
        self.server.close()
