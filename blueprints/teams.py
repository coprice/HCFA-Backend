from sanic.response import json as json_response
from sanic import Blueprint

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

# POST - /courses/request
# {
#     uid: Int,
#     token: String,
#     cid: Int,
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

    mailer.send_message(res['user'][0], res['user'][1], body['message'],
                        res['admins'], 'Ministry Team')

    return json_response(res, status=201)
