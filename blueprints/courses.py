from sanic.response import json as json_response, html, redirect
from sanic import Blueprint

from mailer.mailer import mailer
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

    res = db.create_course(body['uid'], body['token'], body['leader_first'],
                           body['leader_last'], body['year'], body['gender'],
                           body['location'], body['material'], body['meetings'],
                           body['abcls'], body['groupme'], body['members'],
                           body['admins'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

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

    res = db.update_course(body['uid'], body['token'], body['cid'],
                           body['leader_first'], body['leader_last'],
                           body['year'], body['gender'], body['location'],
                           body['material'], body['meetings'], body['abcls'],
                           body['groupme'], body['members'], body['admins'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response(res, status=201)

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

    return json_response(res, status=200)

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

    return json_response(res, status=200)

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
    res = db.send_course_request(uid, body['token'], cid)

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    link = '{}?uid={}&cid={}'.\
        format(request.url.replace('/send', ''), uid, cid)
    mailer.send_message(res['user'][0], res['user'][1], body['message'],
                        'Bible Course', link, res['admins'])

    return json_response({}, status=200)

# GET - /courses/request?uid={uid}&cid={cid}&error={error}
@courses.route(baseURI + '/request', methods=['GET'])
async def display_request(request):
    args = request.args

    if 'uid' not in args or 'cid' not in args:
        return html(template('response.html').\
            render(message='Error: Bad Request', error=True))

    uid, cid = args['uid'][0], args['cid'][0]
    user = db.get_users_info(uid)
    course = db.get_course_info(cid)

    if user is None:
        return html(template('response.html').\
            render(message='Error: User does not exist', error=True))
    if course is None:
        return html(template('response.html').\
            render(message='Error: Course does not exist (or no longer exists)',
                   error=True))

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
            render(message=message, action=action, uid=uid,
                   group_id=cid, id_name='cid', error=args['error'][0]))
    else:
        return html(template('request.html').\
            render(message=message, action=action, uid=uid,
                   group_id=cid, id_name='cid'))

# POST - /courses/request/complete
# {
#     uid: Int,
#     cid: Int,
#     email: String,
#     password: String
# }
@courses.route(baseURI + '/request/complete', methods=['POST'])
async def complete_request(request):
    form = request.form

    if 'uid' not in form or 'cid' not in form or 'email' not in form or \
        'password' not in form:
        return redirect('{}/request/completed?msg={}'.\
            format(baseURI, 'Error: Bad Request'))

    res = db.complete_course_request(form['uid'][0], form['cid'][0],
                                     form['email'][0], form['password'][0])

    if 'error' in res:
        return redirect('{}/request?uid={}&cid={}&error={}'.\
            format(baseURI, uid, cid, res['error']))

    return redirect('{}/request/completed?msg={}'.\
        format(baseURI, 'Success! User was added to the course.'))

# GET - /courses/request/completed?msg={message}
@courses.route(baseURI + '/request/completed', methods=['GET'])
async def completed(request):
    args = request.args

    if 'msg' not in args:
        return html(template('response.html').\
            render(message='Error: Bad Request', error=True))

    return html(template('response.html').\
        render(message=args['msg'][0]))
