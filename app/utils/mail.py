from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self, to_email, subject, body):
        self.to_email = to_email
        self.msg = MIMEMultipart()
        self.msg['To'] = to_email
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(body))

    def set_attachment(self, filename, payload):
        attachment = MIMEApplication(payload)
        attachment.add_header(
            'Content-Disposition', f'attachment; filename={filename}')
        self.msg.attach(attachment)

    def get_from(self):
        return self.msg.get('From', None)

    def get_to(self):
        return self.msg.get('To', None)

    def set_from(self, from_email):
        self.msg['From'] = from_email

    def as_string(self):
        return self.msg.as_string()

    def __str__(self):
        from_str = self.get('From', '')
        to_str = self.msg.get('To', '')
        subject = self.msg.get('Subject', '')
        return f'<From: {from_str}, To: {to_str}, Subject: {subject}>'
