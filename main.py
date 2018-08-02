from sanic import Sanic

from blueprints.users import users
from blueprints.events import events
from blueprints.courses import courses
from blueprints.teams import teams
from blueprints.healthcheck import healthcheck


app = Sanic()
app.blueprint(users)
app.blueprint(events)
app.blueprint(courses)
app.blueprint(teams)
app.blueprint(healthcheck)

if __name__ == "__main__":
    print('Starting up hcfa_app server...')
    app.run(host="0.0.0.0", port=8080)
