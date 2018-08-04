from sanic.response import json as json_response, html, redirect
from sanic import Blueprint

from mailer.mailer import mailer
from template_loader.template_loader import template
from db.db import db


teams = Blueprint('teams')
baseURI = '/teams'

# GET = /teams?uid={uid}&token={token}
@teams.route(baseURI, methods=['GET'])
async def get_teams(request):
    args = request.args

    if 'uid' not in args or 'token' not in args:
        return json_response({'error': 'Bad Request'}, status=400)

    uid = None
    try:
        uid = int(args['uid'][0])
    except:
        return json_response({'error': 'Bad Request'}, status=400)

    res = db.get_teams(uid, args['token'][0])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response(res, status=200)

# POST = /teams/create
# {
#     uid: Int,
#     token: String,
#     name: String,
#     description: String,
#     leaders: String,
#     meetings: [Optional] {String:String},
#     members: [String],
#     admins: [String]
# }
@teams.route(baseURI + '/create', methods=['POST'])
async def create_team(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'name' not in body or \
        'description' not in body or 'leaders' not in body or \
        'meetings' not in body or 'groupme' not in body or \
        'members' not in body or 'admins' not in body:
        return json_response({'error': 'Bad Request'}, status=400)

    res = db.create_team(body['uid'], body['token'], body['name'],
                         body['description'], body['leaders'], body['meetings'],
                         body['groupme'], body['members'], body['admins'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response(res, status=201)

# POST = /teams/update
# {
#     uid: Int,
#     token: String,
#     tid: Int,
#     name: String,
#     description: String,
#     leaders: String,
#     meetings: [Optional] {String:String},
#     members: [String],
#     admins: [String]
# }
@teams.route(baseURI + '/update', methods=['POST'])
async def update_team(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'tid' not in body or \
        'name' not in body or 'description' not in body or \
        'leaders' not in body or 'meetings' not in body or \
        'groupme' not in body or 'members' not in body or 'admins' not in body:
        return json_response({'error': 'Bad Request'}, status=400)


    res = db.update_team(body['uid'], body['token'], body['tid'], body['name'],
                         body['description'], body['leaders'], body['meetings'],
                         body['groupme'], body['members'], body['admins'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response(res, status=200)

# POST = /teams/delete
# {
#     uid: Int,
#     token: String,
#     tid: Int,
# }
@teams.route(baseURI + '/delete', methods=['POST'])
async def delete_team(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'tid' not in body:
        return json_response({'error': 'Bad Request'}, status=400)

    res = db.delete_team(body['uid'], body['token'], body['tid'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response(res, status=200)

# POST - /teams/leave
# {
#     uid: Int,
#     token: String,
#     tid: Int
# }
@teams.route(baseURI + '/leave', methods=['POST'])
async def leave_team(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'tid' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    res = db.leave_team(body['uid'], body['token'], body['tid'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    return json_response(res, status=200)

# POST - /teams/request/send
# {
#     uid: Int,
#     token: String,
#     tid: Int,
#     message: [Optional] String
# }
@teams.route(baseURI + '/request/send', methods=['POST'])
async def send_team_request(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'tid' not in body or \
        'message' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    uid, tid = body['uid'], body['tid']
    res = db.send_team_request(uid, body['token'], tid)

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    link = '{}?uid={}&tid={}&token={}'.\
        format(request.url.replace('/send', ''), uid, tid, res['token'])
    mailer.send_message(res['user'][0], res['user'][1], body['message'],
                        'Ministry Team', link, res['admins'])

    return json_response({}, status=201)

# GET - /teams/request?uid={uid}&tid={tid}&error={error}
@teams.route(baseURI + '/request', methods=['GET'])
async def display_request(request):
    args = request.args

    if 'uid' not in args or 'tid' not in args or 'token' not in args:
        return html(template('response.html').\
            render(message='Error: Bad Request', error=True))

    uid, tid, token = args['uid'][0], args['tid'][0], args['token'][0]

    if not db.validate_team_request(uid, tid, token):
        return html(template('response.html').\
            render(message='Error: Invalid or expired request', error=True))

    user = db.get_users_info(uid)
    team = db.get_team_info(tid)

    if user is None:
        return html(template('response.html').\
            render(message='Error: User does not exist', error=True))
    if team is None:
        return html(template('response.html').\
            render(message='Error: Team does not exist (or no longer exists)',
                   error=True))

    first, last, email = user
    (name,) = team

    message = 'Sign in to add {} ({} {}) to {}'.format(email, first, last, name)
    action = '{}/request/complete'.format(baseURI)

    if 'error' in args:
        return html(template('request.html').\
            render(message=message, action=action, uid=uid, group_id=tid,
                   token=token, id_name='tid', error=args['error'][0]))
    else:
        return html(template('request.html').\
            render(message=message, action=action, uid=uid, group_id=tid,
                   token=token, id_name='tid'))

# POST - /teams/request/complete
# {
#     uid: Int,
#     tid: Int,
#     email: String,
#     password: String
# }
@teams.route(baseURI + '/request/complete', methods=['POST'])
async def complete_request(request):
    form = request.form

    if 'uid' not in form or 'tid' not in form or 'email' not in form or \
        'password' not in form or 'token' not in form:
        return redirect('{}/request/completed?msg={}'.\
            format(baseURI, 'Error: Bad Request'))

    uid, tid, token = form['uid'][0], form['tid'][0], form['token'][0]

    res = db.complete_team_request(uid, tid, token, form['email'][0],
                                   form['password'][0])

    if 'error' in res:
        return redirect('{}/request?uid={}&tid={}&token={}&error={}'.\
            format(baseURI, uid, tid, token, res['error']))

    return redirect('{}/request/completed?msg={}'.\
        format(baseURI, 'Success! User was added to the team.'))

# GET - /teams/request/completed?msg={message}
@teams.route(baseURI + '/request/completed', methods=['GET'])
async def completed(request):
    args = request.args

    if 'msg' not in args:
        return html(template('response.html').\
            render(message='Error: Bad Request', error=True))

    return html(template('response.html').render(message=args['msg'][0]))
