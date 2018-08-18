from sanic import Sanic
from sanic.response import html, redirect
from sanic.exceptions import NotFound

from blueprints.users import users
from blueprints.events import events
from blueprints.courses import courses
from blueprints.teams import teams
from blueprints.healthcheck import healthcheck
from validator.validator import is_http
from template_loader.template_loader import template


app = Sanic()

app.static('/static', './static')
app.blueprint(users)
app.blueprint(events)
app.blueprint(courses)
app.blueprint(teams)
app.blueprint(healthcheck)

@app.middleware('request')
async def redirect_host_urls(request):
    if 'localhost' in request.url:
        return None
    if is_http(request):
        return redirect('https://' + request.url[len('http://'):])

@app.exception(NotFound)
async def notfound(request, exception):
    return redirect('/')

@app.route('/')
async def index(request):
    return html(template('index.html').render())

if __name__ == "__main__":
    print('Starting up hcfa_app server...')
    app.run(host="0.0.0.0", port=8080)
