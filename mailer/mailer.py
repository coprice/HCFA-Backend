import requests

class Mailer:
    def __init__(self):
        pass

    def send_request(self, name, email, message, request_type, link, admins):
        text =\
            "Name: {}\nEmail: {}\nMessage: {}\n\nAdd user to this {} here: {}".\
            format(name, email, message, request_type.lower(), link)

        for admin_name, admin_email in admins:
            requests.post(
                "https://api.mailgun.net/v3/sandbox6cbe982fa9b64efe8110a44cad8f25a7.mailgun.org/messages",
                auth=("api", "key-d31ba89312af933035576be061244371"),
                data={"from": "Mailgun Sandbox <postmaster@sandbox6cbe982fa9b64efe8110a44cad8f25a7.mailgun.org>",
                      "to": "{} <{}>".format(admin_name, admin_email),
                      "subject": "HCFA App: {} Request".format(request_type),
                      "text": text})

    def send_reset(self, email, link):
        requests.post(
            "https://api.mailgun.net/v3/sandbox6cbe982fa9b64efe8110a44cad8f25a7.mailgun.org/messages",
            auth=("api", "key-d31ba89312af933035576be061244371"),
            data={"from": "Mailgun Sandbox <postmaster@sandbox6cbe982fa9b64efe8110a44cad8f25a7.mailgun.org>",
                  "to": "<{}>".format(email),
                  "subject": "HCFA App: Password Reset",
                  "text": "Reset your password here: {}".format(link)})

mailer = Mailer()
