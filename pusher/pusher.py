from time import time
from apns.apns import APNs, Frame, Payload
from config.config import config


class Pusher(object):

    def __init__(self):
        self.cert = config.cert_file
        self.key = config.key_file
        self.use_sandbox = not config.is_prod(config.env)
        self.reset_connection()

    def reset_connection(self):
        self.apns = APNs(use_sandbox=self.use_sandbox, cert_file=self.cert,
                         key_file=self.key)
        self.stamp = time()
        self.failed = set()
        for token, _ in self.apns.feedback_server.items():
            self.failed.add(token)

    def send_notifications(self, tokens, message, category):
        if time() - self.stamp > 86400:
            self.reset_connection()

        rejected_tokens = []
        payload = Payload(alert=message, sound='default', badge=1,
                          mutable_content=True, category=category)
        frame = Frame()
        identifier = 1
        expiry = int(time()) + 3600
        priority = 10
        for token in tokens:
            if token in self.failed:
                rejected_tokens.append(token)
            else:
                frame.add_item(token, payload, identifier, expiry, priority)
        self.failed = set()

        if len(rejected_tokens) != len(tokens):
            try:
                self.apns.gateway_server.send_notification_multiple(frame)
            except:
                self.reset_connection()
                self.apns.gateway_server.send_notification_multiple(frame)

        return rejected_tokens


pusher = Pusher()
