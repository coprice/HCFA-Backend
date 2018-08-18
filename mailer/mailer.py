import smtplib

from config.config import config


class Mailer:
    def __init__(self):
        self.user = config.mailer_email
        self.password = config.mailer_password

    def reset_connection(self):
        self.server = smtplib.SMTP_SSL('smtp.gmail.com')
        self.server.login(self.user, self.password)

    def send_request(self, name, email, message, request_type, link, admins, title):
        self.reset_connection()

        if message:
            message = message.replace("’", "'").replace('“', '"').replace('”', '"')
            message = ''.join(i for i in message if ord(i) < 128) # remove non-ASCII

        msg = """{}: {}\nName: {}\nEmail: {}\nMessage: {}\n\nSign in at the following link to add this user to the {}:\n\n{}""".\
            format(request_type, title, name, email, message, request_type.lower(), link)
        subject = '{} Request'.format(request_type)

        text = "From: {}\r\nTo: {}\r\nSubject: [NO REPLY] {}\r\n\r\n{}".\
            format(self.user, ', '.join(admins), subject, msg)

        try:
            self.server.sendmail(self.user, admins, text)
            self.server.quit()
            return True
        except:
            self.server.quit()
            return False

    def send_reset(self, email, link):
        self.reset_connection()

        msg = "Reset your password at the following link:\n\n{}".format(link)
        text = "From: {}\r\nTo: {}\r\nSubject: [NO REPLY] Password Reset\r\n\r\n{}".\
            format(self.user, email, msg)

        try:
            self.server.sendmail(self.user, email, text)
            self.server.quit()
            return True
        except:
            self.server.quit()
            return False


mailer = Mailer()
