# HCFA Backend

### running locally
* run a postgresql database named `hcfa_app` with the tables specified in `tables.sql`
* install python 3
* create a virtual environment: `virtualenv -p python3 venv`
* run the virtualenv: `source ven/bin/activate`
* install the dependencies: `pip3 install -r requirements.txt`
* run the server: `python3 main.py`

### deploying
* clone [ecs-deploy](https://github.com/silinternational/ecs-deploy) into a *~*/src folder
* run `bash deploy.sh testing | production`
