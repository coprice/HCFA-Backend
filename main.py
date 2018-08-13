from sanic import Sanic

from blueprints.users import users
from blueprints.events import events
from blueprints.courses import courses
from blueprints.teams import teams
from blueprints.healthcheck import healthcheck
from validator.validator import is_http


app = Sanic()

app.static('/static', './static')

@app.middleware('request')
async def redirect_host_urls(request):
    if 'localhost' in request.url:
        return None
    if is_http(request):
        return redirect('https://' + request.url[len('http://'):])

app.blueprint(users)
app.blueprint(events)
app.blueprint(courses)
app.blueprint(teams)
app.blueprint(healthcheck)

if __name__ == "__main__":
    print('Starting up hcfa_app server...')
    app.run(host="0.0.0.0", port=8080)
