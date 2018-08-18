from sanic.response import json as json_response, html, redirect
from sanic import Blueprint

from mailer.mailer import mailer
from pusher.pusher import pusher
from template_loader.template_loader import template
from db.db import db


courses = Blueprint('courses')
baseURI = '/courses'

# GET - /courses?uid={uid}&token={token}
@courses.route(baseURI, methods=['GET'])
async def get_courses(request):

    args = request.args

    if 'uid' not in args or 'token' not in args:
        return json_response({'error': 'Bad request'}, status=400)

    res = db.get_courses(args['uid'][0], args['token'][0])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response(res, status=200)

# POST - /courses/create
# {
#     uid: Int,
#     token: String,
#     leader_first: string,
#     leader_last: string,
#     year: string,
#     gender: string,
#     location: string,
#     material: string,
#     meetings: [optional] {string:string}
#     members: [string],
#     admins: [string]
# }
@courses.route(baseURI + '/create', methods=['POST'])
async def create_course(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or \
        'leader_first' not in body or 'leader_last' not in body or \
        'year' not in body or 'gender' not in body or \
        'location' not in body or 'material' not in body or \
        'meetings' not in body or 'abcls' not in body or \
        'groupme' not in body or 'members' not in body or 'admins' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    leader, year, gender = body['leader_first'], body['year'], body['gender']

    res = db.create_course(body['uid'], body['token'], leader,
                           body['leader_last'], year, gender, body['location'],
                           body['material'], body['meetings'], body['abcls'],
                           body['groupme'], body['members'], body['admins'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    ids = res['members'] + res['admins']

    if leader.endswith('s'):
        leader += "'"
    else:
        leader += "'s"

    msg = 'You\'ve been added to {} {} {}!'.format(leader, year, gender)
    rejected_tokens = pusher.send_notifications(db.get_course_apn_tokens(ids),
                                                msg, 'course')

    for apn_token in rejected_tokens:
        db.remove_apn_token(apn_token)

    return json_response(res, status=201)

# POST - /courses/update
# {
#     uid: Int,
#     token: String,
#     cid: Int
#     leader_first: string,
#     leader_last: string,
#     year: string,
#     gender: string,
#     location: string,
#     material: string,
#     meetings: [optional] {string:string}
#     members: [string],
#     admins: [string]
# }
@courses.route(baseURI + '/update', methods=['POST'])
async def update_course(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'cid' not in body or \
        'leader_first' not in body or 'leader_last' not in body or \
        'year' not in body or 'gender' not in body or \
        'location' not in body or 'material' not in body or \
        'meetings' not in body or 'abcls' not in body or \
        'groupme' not in body or 'members' not in body or 'admins' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    leader, year, gender = body['leader_first'], body['year'], body['gender']

    res = db.update_course(body['uid'], body['token'], body['cid'],
                           leader, body['leader_last'], year, gender,
                           body['location'], body['material'], body['meetings'],
                           body['abcls'], body['groupme'], body['members'],
                           body['admins'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    if leader.endswith('s'):
        leader += "'"
    else:
        leader += "'s"

    tokens = db.get_course_apn_tokens(res['new_members'])

    msg = 'You\'ve been added to {} {} {}!'.format(leader, year, gender)
    rejected_tokens = pusher.send_notifications(tokens, msg, 'course')

    for apn_token in rejected_tokens:
        db.remove_apn_token(apn_token)

    return json_response({}, status=201)

# POST - /courses/delete
# {
#     uid: Int,
#     token: String,
#     cid: Int
# }
@courses.route(baseURI + '/delete', methods=['POST'])
async def delete_course(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'cid' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    res = db.delete_course(body['uid'], body['token'], body['cid'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response({}, status=200)

# POST - /courses/leave
# {
#     uid: Int,
#     token: String,
#     cid: Int
# }
@courses.route(baseURI + '/leave', methods=['POST'])
async def leave_course(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'cid' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    res = db.leave_course(body['uid'], body['token'], body['cid'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response({}, status=200)

# POST - /courses/request/send
# {
#     uid: Int,
#     token: String,
#     cid: Int,
#     message: [Optional] String
# }
@courses.route(baseURI + '/request/send', methods=['POST'])
async def send_course_request(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'cid' not in body or \
        'message' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    uid, cid = body['uid'], body['cid']
    res = db.prepare_course_request(uid, body['token'], cid)

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    link = '{}?uid={}&cid={}&token={}'.\
        format(request.url.replace('/send', ''), uid, cid, res['token'])

    course = db.get_course_info(cid)
    if course is None:
        return json_response({'error': 'Bible course not found'}, status=404)

    leader, year, gender = course
    if leader.endswith('s'):
        leader += "'"
    else:
        leader += "'s"
    title = '{} {} {}'.format(leader, year, gender)

    sent = mailer.send_request(res['user'][0], res['user'][1], body['message'],
                               'Bible Course', link, res['admins'], title)

    if not sent:
        json_response({'error': 'Unable to send email'}, status=500)

    return json_response({}, status=200)

# GET - /courses/request?uid={uid}&cid={cid}&token={token}&error={error}
@courses.route(baseURI + '/request', methods=['GET'])
async def display_request(request):
    args = request.args

    if 'uid' not in args or 'cid' not in args or 'token' not in args:
        return html(template('response.html').\
            render(message='Error: Bad Request', error=True))

    uid, cid, token = args['uid'][0], args['cid'][0], args['token'][0]

    if not db.validate_course_request(uid, cid, token):
        return html(template('response.html').\
            render(message='Error: Invalid or expired request', error=True))

    user = db.get_users_info(uid)
    course = db.get_course_info(cid)

    if user is None:
        return html(template('response.html').\
            render(message='Error: User no longer exists', error=True))
    if course is None:
        return html(template('response.html').\
            render(message='Error: Course no longer exists', error=True))

    first, last, email = user
    leader, year, gender = course

    if leader.endswith('s'):
        leader += "'"
    else:
        leader += "'s"

    message = 'Sign in to add {} ({} {}) to {} {} {}'.format(email, first, last,
                                                   leader, year, gender)
    action = '{}/request/complete'.format(baseURI)

    if 'error' in args:
        return html(template('request.html').\
            render(message=message, action=action, uid=uid, group_id=cid,
                   token=token, id_name='cid', error=args['error'][0]))
    else:
        return html(template('request.html').\
            render(message=message, action=action, uid=uid, group_id=cid,
                   token=token, id_name='cid'))

# POST - /courses/request/complete
# {
#     uid: Int,
#     cid: Int,
#     email: String,
#     password: String,
#     token: String
# }
@courses.route(baseURI + '/request/complete', methods=['POST'])
async def complete_request(request):
    form = request.form

    if 'uid' not in form or 'cid' not in form or 'email' not in form or \
        'password' not in form or 'token' not in form:
        return redirect('{}/request/completed?msg={}'.\
            format(baseURI, 'Error: Bad Request'))

    uid, cid, token = form['uid'][0], form['cid'][0], form['token'][0]

    res = db.complete_course_request(uid, cid, token, form['email'][0],
                                     form['password'][0])
    course = db.get_course_info(cid)

    error = None
    if 'error' in res:
        error = res['error']
    elif course is None:
        error = 'Bible course no longer exists'

    if error:
        return redirect('{}/request?uid={}&cid={}&token={}&error={}'.\
            format(baseURI, uid, cid, token, error))

    leader, year, gender = course
    if leader.endswith('s'):
        leader += "'"
    else:
        leader += "'s"
    msg = 'You\'ve been added to {} {} {}!'.format(leader, year, gender)

    rejected_tokens = pusher.send_notifications(db.get_course_apn_tokens([uid]),
                                                msg, 'course')

    for apn_token in rejected_tokens:
        db.remove_apn_token(apn_token)

    return redirect('{}/request/completed?msg={}'.\
        format(baseURI, 'Success! User was added to the course.'))

# GET - /courses/request/completed?msg={message}
@courses.route(baseURI + '/request/completed', methods=['GET'])
async def completed(request):
    args = request.args

    if 'msg' not in args:
        return html(template('response.html').\
            render(message='Error: Bad Request', error=True))

    message = args['msg'][0]
    return html(template('response.html').\
        render(message=message, error=message.startswith('Error')))
