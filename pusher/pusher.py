import time
from apns import APNs, Frame, Payload

class Pusher(object):

    def __init__(self):
        print('Opening connection to APNS...')
        self.apns = APNs(use_sandbox=True, cert_file='pems/aps_dev_cert.pem', key_file='pems/aps_dev_key_decrypted.pem')
        for token_hex, fail_time in self.apns.feedback_server.items():
            print('token: {}. fail_time: {}'.format(token_hex, fail_time))

    def reset_connection(self):
        self.apns = APNs(use_sandbox=True, cert_file='pems/aps_dev_cert.pem', key_file='pems/aps_dev_key_decrypted.pem')

    def send_event_notifications(self, event):
        payload = Payload(alert="A new event has been added! Check it out: {}".
                          format(event),
                          sound="default", badge=1)
        frame = Frame()
        identifier = 1
        expiry = time.time()+3600
        priority = 10
        for token, fail_time in self.apns.feedback_server.items():
            frame.add_item(token, payload, identifier, expiry, priority)
        apns.gateway_server.send_notification_multiple(frame)

pusher = Pusher()