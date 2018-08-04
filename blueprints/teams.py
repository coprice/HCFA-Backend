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

# POST - /teams/request
# {
#     uid: Int,
#     token: String,
#     tid: Int,
#     message: [Optional] String
# }
@teams.route(baseURI + '/request/prepare', methods=['POST'])
async def prepare_team_request(request):
    body = request.json

    if 'uid' not in body or 'token' not in body or 'tid' not in body or \
        'message' not in body:
        return json_response({'error': 'Bad request'}, status=400)

    res = db.prepare_team_request(body['uid'], body['token'], body['tid'])

    if 'error' in res:
        return json_response({'error': res['error']}, status=res['status'])

    link = '0.0.0.0:8080{}/request?uid={}&tid={}'.format(baseURI, uid, tid)
    mailer.send_message(res['user'][0], res['user'][1], body['message'],
                        res['admins'], 'Ministry Team', link)

    return json_response(res, status=201)

# GET - /teams/request?uid={uid}&tid={tid}&error={error}
@teams.route(baseURI + '/request', methods=['GET'])
async def display_request(request):
    args = request.args

    if 'uid' not in args or 'tid' not in args:
        return html(template('response.html').\
            render(message='Error: Bad Request', error=True))

    user = db.get_users_info(args['uid'][0])
    team = db.get_team_info(args['tid'][0])

    if user is None:
        return html(template('response.html').\
            render(message='Error: User does not exist', error=True))
    if team is None:
        return html(template('response.html').\
            render(message='Error: Team does not exist', error=True))

    first, last, email = user
    (name,) = team

    message = 'Add {} ({} {}) to {}?'.format(email, first, last, name)
    action = '{}/request/complete'.format(baseURI)

    if 'error' in args:
        return html(template('request.html').\
            render(message=message, action=action, uid=uid,
                   group_id=tid, id_name='tid', error=args['error'][0]))
    else:
        return html(template('request.html').\
            render(message=message, action=action, uid=uid,
                   group_id=tid, id_name='tid'))

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
        'password' not in form:
        return redirect('{}/request/completed?msg={}'.\
            format(baseURI, 'Error: Bad Request'))

    res = db.complete_team_request(form['uid'][0], form['tid'][0],
                                   form['email'][0], form['password'][0])

    if 'error' in res:
        return redirect('{}/request?uid={}&tid={}&error={}'.\
            format(baseURI, uid, tid, res['error']))

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
