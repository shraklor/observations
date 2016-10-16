import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import security
import datetime


class GMailer(object):
    def __init__(self, configuration):
        config = configuration['email.smtp']

        sslPort = config['ssl']
        if len(sslPort) > 0:
            sslPort = security.Security.decrypt(sslPort)
            self.sslPort = int(sslPort)

        server = config['server']
        if len(server) > 0:
            self.server = security.Security.decrypt(server)

        username = config['username']
        if len(username) > 0:
            self.username = security.Security.decrypt(username)

        user = config['user']
        if len(user) > 0:
            self.user = security.Security.decrypt(user)

        password = config['password']
        if len(password) > 0:
            self.password = security.Security.decrypt(password)

    def send(self, config, camera, image):
        msg = MIMEMultipart('mixed')
        msg['From'] = self.username
        msg['To'] = config['email']

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        subject = config['subject']
        subject = subject.replace('{CAMERA}', camera).replace('{TIME}', now)
        msg['Subject'] = subject

        body = config['body']
        body = body.replace('{CAMERA}', camera).replace('{TIME}', now)
        msg.preamble = body
        textPart = MIMEText(body, 'plain')
        msg.attach(textPart)

        if image is not None:
            fp = open(image, 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            msg.attach(img)

        sender = smtplib.SMTP_SSL()
        sender.connect(self.server, self.sslPort)
        sender.ehlo()
        sender.login(self.user, self.password)
        sender.sendmail(self.username, [config['email']], msg.as_string())
        sender.close()

