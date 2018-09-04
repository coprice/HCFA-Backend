from sanic.response import json as json_response
from sanic import Blueprint
from datetime import datetime
from humanize import number

from db.db import db
from pusher.pusher import pusher


events = Blueprint('events')
baseURI = '/events'

# GET = /events
@events.route(baseURI, methods=['GET'])
async def get_events(request):
    return json_response(db.get_events(), status=200)

# POST = /events/create
# {
#     uid: Int,
#     token: String,
#     title: String,
#     location: String,
#     start: String,
#     end: String,
#     description: String,
#     image: [Optional] String
# }
@events.route(baseURI + '/create', methods=['POST'])
async def create_event(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'title' not in body or \
        'location' not in body or 'start' not in body or 'end' not in body \
        or 'description' not in body or 'image' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    title = body['title']

    res = db.create_event(body['uid'], body['token'], title, \
                          body['location'], body['start'], \
                          body['end'], body['description'], body['image'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    msg = 'A new event ({}) has been added! Check it out!'.format(title)
    rejected_tokens = pusher.send_notifications(db.get_event_apn_tokens(),
                                                msg, 'event')

    for apn_token in rejected_tokens:
        db.remove_apn_token(apn_token)

    return json_response(res, status=201)

# POST = /events/update
# {
#     uid: Int,
#     token: String,
#     eid: Int,
#     title: String,
#     location: String,
#     start: String,
#     end: String,
#     description: String,
#     image: [Optional] String
# }
@events.route(baseURI + '/update', methods=['POST'])
async def update_event(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'eid' not in body or \
        'title' not in body or 'location' not in body or \
        'start' not in body or 'end' not in body or \
        'description' not in body or 'image' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    title, start, end = body['title'], body['start'], body['end']
    res = db.update_event(body['uid'], body['token'], body['eid'],
                          title, body['location'], start, end,
                          body['description'], body['image'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    start_dt = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    end_dt = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')

    start_dt_old = datetime.strptime(res['start_old'], '%Y-%m-%d %H:%M:%S')
    end_dt_old = datetime.strptime(res['end_old'], '%Y-%m-%d %H:%M:%S')

    if start_dt != start_dt_old or end_dt != end_dt_old:

        msg = 'The time of {} has been changed. It will now '.format(title)
        start_time_str = start_dt.strftime('%I:%M%p').lstrip('0').lower()
        end_time_str = end_dt.strftime('%I:%M%p').lstrip('0').lower()

        if start_dt.date() == end_dt.date():
            day = start_dt.strftime('%A, %B ')
            day += number.ordinal(start_dt.day)
            msg += 'be from {} to {} on {}.'.format(start_time_str,
                                                    end_time_str, day)
        else:
            start_day = start_dt.strftime('%A, %B ')
            start_day += number.ordinal(start_dt.day)
            end_day = end_dt.strftime('%A, %B ')
            end_day += number.ordinal(end_dt.day)

            msg += 'start on {} at {} and end on {} at {}.'.\
                format(start_day, start_time_str, end_day, end_time_str)

        rejected_tokens = pusher.send_notifications(db.get_event_apn_tokens(),
                                                    msg, 'event')
        for apn_token in rejected_tokens:
            db.remove_apn_token(apn_token)

    return json_response({}, status=201)

# POST = /events/delete
# {
#     uid: Int,
#     token: String,
#     eid: Int,
# }
@events.route(baseURI + '/delete', methods=['POST'])
async def delete_events(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'events' not in body:
        return json_response({'error': 'Bad request' }, status=400)

    res = db.delete_events(body['uid'], body['token'], body['events'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response({}, status=200)
