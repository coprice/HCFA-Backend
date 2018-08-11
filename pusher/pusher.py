from time import time
from apns.apns import APNs, Frame, Payload
from config.config import config

class Pusher(object):

    def __init__(self):
        print('Opening connection to APNS...')
        self.cert = config.cert_file
        self.key = config.key_file
        self.reset_connection()

    def reset_connection(self):
        self.apns = APNs(use_sandbox=True, cert_file=self.cert,
                         key_file=self.key)
        self.stamp = time()
        self.failed = set()
        for token, _ in self.apns.feedback_server.items():
            self.failed.add(token)

    def reset_if_necessary(self):
        if time() - self.stamp > 86400:
            self.reset_connection()

    def send_notification(self, token, message):
        self.reset_if_necessary()

        if token in self.failed:
            return token
        else:
            payload = Payload(alert=message, sound='default',
                              badge=1, mutable_content=True)
            self.apns.gateway_server.send_notification(token, payload)

    def send_notifications(self, tokens, message):
        self.reset_if_necessary()

        rejected_tokens = []
        payload = Payload(alert=message, sound='default', badge=1,
                          mutable_content=True)
        frame = Frame()
        identifier = 1
        expiry = int(time()) + 3600
        priority = 10
        for token in tokens:
            if token in self.failed:
                rejected_tokens.append(token)
            else:
                frame.add_item(token, payload, identifier, expiry, priority)

        if len(rejected_tokens) != len(tokens):
            self.apns.gateway_server.send_notification_multiple(frame)

        return rejected_tokens

pusher = Pusher()
