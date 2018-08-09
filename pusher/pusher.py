import time
from apns import APNs, Frame, Payload

class Pusher(object):

    def __init__(self):
        self.apns = APNs(use_sandbox=True, cert_file='cert.pem', key_file='key.pem')
        for token_hex, fail_time in feedback_connection.feedback_server.items():
            print('token: {}. fail_time: {}'.format(token_hex, fail_time))

    def reset_connection(self):
        self.apns = APNs(use_sandbox=True, cert_file='cert.pem', key_file='key.pem')

    def send_event_notifications(self, tokens, event):
        payload = Payload(alert="A new event has been added! Check it out: {}".
                          format(event),
                          sound="default", badge=1)
        frame = Frame()
        identifier = 1
        expiry = time.time()+3600
        priority = 10
        for token in tokens:
            frame.add_item(token, payload, identifier, expiry, priority)
        apns.gateway_server.send_notification_multiple(frame)

pusher = Pusher()