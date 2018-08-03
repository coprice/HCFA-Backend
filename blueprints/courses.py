from sanic.response import json as json_response, html
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

    uid = None
    try:
        uid = int(args['uid'][0])
    except:
        return json_response({'error': 'Bad request'}, status=400)

    res = db.get_courses(uid, args['token'][0])

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

# POST - /courses/request
# {
#     uid: Int,
#     token: String,
#     cid: Int,
#     message: [Optional] String
# }
@courses.route(baseURI + '/request/prepare', methods=['POST'])
async def prepare_course_request(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'cid' not in body or \
        'message' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    res = db.prepare_course_request(body['uid'], body['token'], body['cid'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    mailer.send_message(res['user'][0], res['user'][1], body['message'],
                        res['admins'], 'Bible Course')

    return json_response({}, status=200)

# GET - /courses/request?uid={uid}&cid={cid}
@courses.route(baseURI + '/request', methods=['GET'])
async def display_request(request):
    args = request.args

    if 'uid' not in args or 'cid' not in args:
        return html('Bad request')

    uid, cid = None, None

    try:
        uid, cid = int(args['uid'][0]), int(args['cid'][0])
    except:
        return html('Bad request')

    user = db.get_users_info(uid)
    course = db.get_course_info(cid)

    if user is None:
        return html('User does not exist')
    if course is None:
        return html('Course does not exist')

    first, last, email = user
    leader, year, gender = course

    if leader.endswith('s'):
        leader += "'"
    else:
        leader += "'s"

    message = 'Add {} ({} {}) to {} {} {}?'.format(email, first, last,
                                                   leader, year, gender)

    return html(template('request.html').render(message=message, base='courses'))

# POST - /courses/request/complete
# {
#     uid: Int,
#     cid: Int,
#     email: String,
#     password: String
# }
@courses.route(baseURI + '/request/complete', methods=['POST'])
async def complete_request(request):
    body = request.json

    if 'uid' not in body or 'cid' not in body or 'email' not in body or \
        'password' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    uid, cid = None, None

    try:
        uid, cid = int(body['uid']), int(body['cid'])
    except:
        return json_response({'error': 'Bad request'}, status=400)

    res = db.complete_course_request(body['uid'], body['cid'],
                                     body['email'], body['password'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=200)

    return json_response(res, status=200)
