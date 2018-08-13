import smtplib

from config.config import config


class Mailer:
    def __init__(self):
        self.user = config.mailer_email
        self.password = config.mailer_password

    def send_request(self, name, email, message, request_type, link, admins, title):
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.login(self.user, self.password)

        msg = "{}: {}\nName: {}\nEmail: {}\nMessage: {}\n\nClick the following link to add this user to the {}:\n\n{}".\
            format(request_type, title, name, email, message, request_type.lower(), link)
        subject = '{} Request'.format(request_type)

        text = "From: {}\r\nTo: {}\r\nSubject: [NO REPLY] {}\r\n\r\n{}".\
            format(self.user, ', '.join(admins), subject, msg)

        try:
            server.sendmail(self.user, admins, text)
            return True
        except:
            return False

    def send_reset(self, email, link):
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.login(self.user, self.password)

        msg = "Reset your password here: {}".format(link)
        text = "From: {}\r\nTo: {}\r\nSubject: [NO REPLY] Password Reset\r\n\r\n{}".\
            format(self.user, email, msg)

        try:
            server.sendmail(self.user, email, text)
            return True
        except:
            return False


mailer = Mailer()
