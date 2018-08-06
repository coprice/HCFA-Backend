from sanic.response import json as json_response, html, redirect
from sanic import Blueprint

from mailer.mailer import mailer
from template_loader.template_loader import template
from db.db import db


users = Blueprint('users')
baseURI = '/users'

# POST - /users/register
# {
#     first_name: string,
#     last_name: string,
#     email: string,
#     password: string
# }
@users.route(baseURI + '/register', methods=['POST'])
async def register_user(request):
    body = request.json

    if 'first_name' not in body or 'last_name' not in body or \
        'email' not in body or 'password' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    res = db.register_user(body['first_name'], body['last_name'],
                           body['email'], body['password'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response(res, status=201)

# GET - /users/login?email={email}&password={password}
# {
#     email: string,
#     password: string
# }
@users.route(baseURI + '/login', methods=['GET'])
async def login_user(request):
    args = request.args

    if 'email' not in args or 'password' not in args:
        return json_response({'error': 'Bad request'}, status=400)

    res = db.login_user(args['email'][0], args['password'][0])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response(res, status=200)

# GET - /users/validate?uid={uid}&token={token}
# {
#     uid: int,
#     token: string
# }
@users.route(baseURI + '/validate', methods=['GET'])
async def validate_session(request):
    args = request.args

    if 'uid' not in args or 'token' not in args:
        return json_response({'error': 'Bad request'}, status=400)

    uid = None
    try:
        uid = int(args['uid'][0])
    except:
        return json_response({'error': 'Bad request'}, status=400)

    if db.validate_session(uid, args['token'][0]):
        return json_response({}, status=200)
    else:
        return json_response({'error': 'Session Expired'}, status=403)

# POST - /users/leader/add
# {
#     uid: int
#     token: string
#     email: string
# }
@users.route(baseURI + '/leader/add', methods=['POST'])
async def add_leader(request):
    body = request.json
    if 'uid' not in body or 'token' not in body or 'email' not in body:
        return json_response({ 'error': 'Bad request' }, status=400)

    res = db.change_permission(body['uid'], body['token'], body['email'],
                               perm='leader', is_add=True)

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response({}, status=201)

# POST - /users/leader/remove
# {
#     uid: int
#     token: string
#     email: string
# }
@users.route(baseURI + '/leader/remove', methods=['POST'])
async def add_leader(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'email' not in body:
        return json_response({ 'error': 'Bad request' }, status=400)

    res = db.change_permission(body['uid'], body['token'], body['email'],
                               perm='leader', is_add=False)

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response({}, status=201)

# POST - /users/admin/add
# {
#     uid: int
#     token: string
#     email: string
# }
@users.route(baseURI + '/admin/add', methods=['POST'])
async def add_admin(request):
    body = request.json
    if 'uid' not in body or 'token' not in body or 'email' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    res = db.change_permission(body['uid'], body['token'], body['email'],
                               perm='admin', is_add=True)

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response({}, status=201)

# POST - /users/admin/remove
# {
#     uid: int
#     token: string
#     email: string
# }
@users.route(baseURI + '/admin/remove', methods=['POST'])
async def remove_admin(request):
    body = request.json
    if 'uid' not in body or 'token' not in body or 'email' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    res = db.change_permission(body['uid'], body['token'], body['email'],
                               perm='admin', is_add=False)

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response({}, status=201)

# POST - /users/update/password
# {
#     uid: int
#     token: string
#     old_password: string
#     new_password: string
# }
@users.route(baseURI + '/update/password', methods=['POST'])
async def change_password(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or \
        'old_password' not in body or 'new_password' not in body:
        return json_response({ 'error': 'Bad request' }, status=400)

    res = db.change_password(body['uid'], body['token'], body['old_password'],
                             body['new_password'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response({}, status=201)

# POST - users/update/contact
# {
#     uid: int,
#     token: int,
#     first: string,
#     last: string,
#     email: string
# }
@users.route(baseURI + '/update/contact', methods=['POST'])
async def update_contact(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'first' not in body or \
        'last' not in body or 'email' not in body:
        return json_response({ 'error': 'Bad request' }, status=400)

    res = db.update_contact(body['uid'], body['token'], body['first'],
                            body['last'], body['email'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response({}, status=201)

# POST - users/update/image
# {
#     uid: int,
#     image: string
# }
@users.route(baseURI + '/update/image', methods=['POST'])
async def update_image(request):
    body = request.json

    if 'uid' not in body or 'token' not in  body or 'image' not in body:
        return json_response({ 'error': 'Bad request' }, status=400)

    res = db.update_image(body['uid'], body['token'], body['image'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response({}, status=201)

# POST - users/reset/send
# {
#     email: String
# }
@users.route(baseURI + '/reset/send', methods=['POST'])
async def send_reset(request):
    body = request.json

    if 'email' not in body:
        return json_response({ 'error': 'Bad request' }, status=400)

    email = body['email']
    res = db.check_email(email)

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    link = '{}?uid={}&token={}'.\
        format(request.url.replace('/send', ''), res['uid'], res['token'])
    mailer.send_reset(email, link)

    return json_response({}, status=201)

# GET - users/reset?uid={uid}&token={token}
@users.route(baseURI + '/reset', methods=['GET'])
async def display_reset(request):
    args = request.args

    if 'uid' not in args or 'token' not in args:
        return html(template('response.html').\
            render(message='Error: Bad Request', error=True))

    uid, token = args['uid'][0], args['token'][0]

    if not db.validate_password_request(uid, token):
        return html(template('response.html').\
            render(message='Error: Invalid or expired request', error=True))

    action = '{}/reset/complete'.format(baseURI)
    return html(template('request.html').\
        render(action=action, uid=uid, token=token))

# POST - users/reset/complete
# {
#     uid: Int,
#     password: String,
#     confirm: String,
#     token: String
# }
@users.route(baseURI + '/reset/complete', methods=['POST'])
async def complete_reset(request):
    form = request.form

    if 'uid' not in form or 'password' not in form or 'confirm' not in form or \
        'token' not in form:
        return redirect('{}/reset/completed?msg={}'.\
            format(baseURI, 'Error: Bad Request'))

    uid, token = form['uid'][0], form['token'][0]

    res = db.complete_password_reset(uid, token, form['password'][0])

    return redirect('{}/request/completed?msg={}'.\
        format(baseURI, 'Success! User was added to the course.'))

# GET - /users/reset/completed?msg={message}
@courses.route(baseURI + '/request/completed', methods=['GET'])
async def completed(request):
    args = request.args

    if 'msg' not in args:
        return html(template('response.html').\
            render(message='Error: Bad Request', error=True))

    message = args['msg'][0]
    return html(template('response.html').\
        render(message=args['msg'][0], error=message.startswith('Error')))
