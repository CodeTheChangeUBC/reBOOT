from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class Mail:
    def __init__(self, to_email, subject, body):
        self.to_email = to_email
        self.msg = MIMEMultipart()
        self.msg['To'] = to_email
        self.msg['Subject'] = subject

    def set_attachment(self, filename, payload):
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(payload)
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition', f'attachment; filename={filename}')
        self.msg.attach(attachment)

    def set_from(self, from_email):
        self.msg['From'] = from_email

    def as_string(self):
        return self.msg.as_string()
