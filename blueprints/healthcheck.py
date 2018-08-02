from sanic.response import json as json_response
from sanic import Blueprint


healthcheck = Blueprint('healthcheck')

@healthcheck.route('/healthcheck', methods=['GET'])
async def health_check(request):
    return json_response({'success': 'shakyamuni bro!'}, status=200)
