from time import time
from apns import APNs, Frame, Payload

class Pusher(object):

    def __init__(self):
        print('Opening connection to APNS...')
        self.apns = APNs(use_sandbox=True,
                         cert_file='pems/aps_dev_cert.pem',
                         key_file='pems/aps_dev_key_decrypted.pem')
        self.stamp = time()
        for token, fail_time in self.apns.feedback_server.items():
            print('token: {}. fail_time: {}'.format(token, fail_time))

    # renews connection to APNs if connection has expired (allow 1 day)
    def reset_if_necessary(self):
        if time() - self.stamp > 86400:
            self.apns = APNs(use_sandbox=True,
                             cert_file='pems/aps_dev_cert.pem',
                             key_file='pems/aps_dev_key_decrypted.pem')
            self.stamp = time()

    def send_notification(self, token, message):
        self.reset_if_necessary()

        payload = Payload(alert=message, sound='default',
                          badge=1, mutable_content=True)
        apns.gateway_server.send_notification(token, payload)

    def send_event_notifications(self, event):
        self.reset_if_necessary()

        payload = Payload(alert="A new event has been added! Check it out: {}".
                          format(event),
                          sound="default", badge=1, mutable_content=True)
        frame = Frame()
        identifier = 1
        expiry = time() + 3600
        priority = 10
        for token, fail_time in self.apns.feedback_server.items():
            frame.add_item(token, payload, identifier, expiry, priority)
        apns.gateway_server.send_notification_multiple(frame)

pusher = Pusher()