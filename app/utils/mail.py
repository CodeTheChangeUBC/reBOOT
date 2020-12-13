from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self, to: str, subject: str, body: str, subtype='mixed'):
        self.to_email = to
        self.msg = MIMEMultipart(subtype)
        self.msg['To'] = to
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(body))

    def get_from(self):
        return self.msg.get('From', None)

    def get_to(self):
        return self.msg.get('To', None)

    def set_from(self, from_email: str):
        self.msg['From'] = from_email

    def as_string(self):
        return self.msg.as_string()

    def set_attachment(self, filename: str, payload: str):
        attachment = MIMEApplication(payload)
        attachment.add_header(
            'Content-Disposition', f'attachment; filename={filename}')
        self.msg.attach(attachment)

    def add_html_body(self, body):
        html = MIMEText(body, 'html')
        self.msg.attach(html)

    def add_embbed_image(self, image_id: str, image_bytes: str):
        '''
        image_id must in the format of "<id_name>"
        '''
        image = MIMEImage(image_bytes)
        image.add_header('Content-ID', image_id)
        self.msg.attach(image)

    def __str__(self):
        from_str = self.get('From', '')
        to_str = self.msg.get('To', '')
        subject = self.msg.get('Subject', '')
        return f'<From: {from_str}, To: {to_str}, Subject: {subject}>'
