import smtplib

class Mailer:
    def __init__(self):
        self.user = 'hcfa.app@gmail.com'
        self.password = '#Doxo1ogy'
        self.server = smtplib.SMTP_SSL('smtp.gmail.com')
        self.server.login(self.user, self.password)

    def send_request(self, name, email, message, request_type, link, admins, title):

        msg = "{}: {}\nName: {}\nEmail: {}\nMessage: {}\n\nClick the following link to add this user to the {}:\n\n{}".\
            format(request_type, title, name, email, message, request_type.lower(), link)
        subject = '{} Request'.format(request_type)

        text = "From: {}\r\nTo: {}\r\nSubject: [NO REPLY] {}\r\n\r\n{}".\
            format(self.user, ', '.join(admins), subject, msg)

        try:
            self.server.sendmail(self.user, admins, text)
            return True
        except:
            return False

    def send_reset(self, email, link):

        msg = "Reset your password here: {}".format(link)
        text = "From: {}\r\nTo: {}\r\nSubject: [NO REPLY] Password Reset\r\n\r\n{}".\
            format(self.user, email, msg)

        try:
            self.server.sendmail(self.user, email, text)
            return True
        except:
            return False

mailer = Mailer()
