import requests

class Mailer:
    def __init__(self):
        pass

    def send_message(self, name, email, message, admins, request_type):

        message_text = "Name: {}\nEmail: {}\nMessage: {}\n\n".format(name, email, message)

        for admin_name, admin_email in admins:

            requests.post(
                "https://api.mailgun.net/v3/sandbox6cbe982fa9b64efe8110a44cad8f25a7.mailgun.org/messages",
                auth=("api", "key-d31ba89312af933035576be061244371"),
                data={"from": "Mailgun Sandbox <postmaster@sandbox6cbe982fa9b64efe8110a44cad8f25a7.mailgun.org>",
                      "to": "{} <{}>".format(admin_name, admin_email),
                      "subject": "HCFA App: {} Request".format(request_type),
                      "text":  message_text})

mailer = Mailer()
