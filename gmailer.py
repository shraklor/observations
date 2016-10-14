import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import security

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

    def send(self, message):
        msg = MIMEMultipart()
        msg['Subject'] = message['subject']
        msg['From'] = self.username
        msg['To'] = message['to']
        msg.preamble = message['body']

        if message['attachment'] is not None:
            fp = open(message['attachment'], 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            msg.attach(img)

        sender = smtplib.SMTP_SSL()
        sender.connect(self.server, self.sslPort)
        sender.ehlo()
        sender.login(self.user, self.password)
        sender.sendmail(self.username, [message['to']], msg.as_string())
        sender.close()

