# HCFA Backend

### running locally
* clone this repository
* install python 3
* run a postgresql database named `hcfa_app` and create the necessary tables with the commands specified in `tables.sql`
* create a virtual environment: `virtualenv -p python3 venv`
* run the virtualenv: `source venv/bin/activate`
* install the dependencies: `pip3 install -r requirements.txt`
* for push notifications, I used PyAPNs, which (as of now) has not updated PyPi to include Python 3 compatibility; to get around this, clone everything from [here](https://github.com/djacobs/PyAPNs/tree/fce9e33c62a0cef8eebcd8b1a293d66be0b45480) and name the cloned repository `apns`
* from the `static` directory, clone the semantic ui css distribution, which can be found [here](https://github.com/Semantic-Org/Semantic-UI-CSS) and name the cloned repository `semantic`
* you might notice some references to a config file and Config class; figure out what that is used for and can make your own
* run the server: `python3 main.py`

### Endpoint Overview

Each endpoint is for the current HCFA app api at [https://hcfa-app.com](https://hcfa-app.com). All responses are JSON and the following documentation assumes no error occurs. If an error occurs in any endpoint a JSON object is returned with an error message saved under the key "error".

Endpoints
======

### POST - /users/register
##### + Creates a new user
**request**:

{

&nbsp;&nbsp;"first_name" : string,

&nbsp;&nbsp;"last_name" : string,

&nbsp;&nbsp;"email" : string,

&nbsp;&nbsp;"password" : string

}

**response**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"first_name" : string,

&nbsp;&nbsp;"last_name" : string,

&nbsp;&nbsp;"email" : string,

&nbsp;&nbsp;"admin" : bool,

&nbsp;&nbsp;"leader" : bool,

&nbsp;&nbsp;"token" : string

}


### GET - /users/login
##### + Logs in an existing user
**arguments**:

{

&nbsp;&nbsp;"email" : string,

&nbsp;&nbsp;"password" : string

}

**response**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"first_name" : string,

&nbsp;&nbsp;"last_name" : string,

&nbsp;&nbsp;"email" : string,

&nbsp;&nbsp;"admin" : bool,

&nbsp;&nbsp;"leader" : bool,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"image" : (optional) string,

&nbsp;&nbsp;"apn_tokens" : [string],

&nbsp;&nbsp;"event_ntf" : bool,

&nbsp;&nbsp;"course_ntf" : bool,

&nbsp;&nbsp;"team_ntf" : bool

}


### GET - /users/validate
##### + Validates a users session
**arguments**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string

}

**response**:

{}


### POST - /users/leader/add
##### + Makes an existing user a leader
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"email" : string

}

**response**:

{}


### POST - /users/leader/remove
##### + Removes an existing leader
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"email" : string

}

**response**:

{}


### POST - /users/admin/add
##### + Makes an existing user an admin
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"email" : string

}

**response**:

{}


### POST - /users/admin/remove
##### + Removes an existing admin
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"email" : string

}

**response**:

{}


### POST - /users/update/password
##### + Updates an existing user's password
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"old_password" : string,

&nbsp;&nbsp;"new_password" : string

}

**response**:

{}


### POST - /users/update/contact
##### + Updates an existing user's contact information
**request**:

{


&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"first" : string,

&nbsp;&nbsp;"last" : string,

&nbsp;&nbsp;"email" : string

}

**response**:

{}


### POST - /users/update/image
##### + Updates an existing user's image
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"image" : string

}

**response**:

{}

### POST - /users/update/notifications
##### + Updates an existing user's notification settings
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"ntf_type" : string,

&nbsp;&nbsp;"ntf_bool" : bool

}

**response**:

{}


### POST - /users/update/apn
##### + Adds an apn token for an existing user
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"apn_token" : string,

}

**response**:

{}


### POST - /users/reset/send
##### + Sends a password reset request to an existing user
**request**:

{

&nbsp;&nbsp;"email" : string

}

**response**:

{}


### GET - /events
##### + Gets all events, past and present
**response**:

{

&nbsp;&nbsp;"upcoming_events" : [

&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"eid" : int,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"title" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"location" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"start" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"end" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"description" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"image" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"repeat" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"end_repeat" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"repeat_days" : (optional) {

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(optional) "1" : {

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(optional) "start" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(optional) "end" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(optional) "location" : string

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(optional) "2" : same as "1"

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(optional) "3" : same as "1"

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(optional) "4" : same as "1"

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(optional) "5" : same as "1"

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(optional) "6" : same as "1"

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(optional) "7" : same as "1"

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;],

&nbsp;&nbsp;"past_events" : same as "upcoming_events",

&nbsp;&nbsp;"repeat_events" : same as "upcoming_events"

}

### POST - /events/create
##### + Creates a new event
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"title" : string,

&nbsp;&nbsp;"location" : string,

&nbsp;&nbsp;"start" : string,

&nbsp;&nbsp;"end" : string,

&nbsp;&nbsp;"description" : string,

&nbsp;&nbsp;"image" : (optional) string

}

**response**:

{

&nbsp;&nbsp;"eid" : int

}

### POST - /events/update
##### + Updates an existing event
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"eid" : int,

&nbsp;&nbsp;"title" : string,

&nbsp;&nbsp;"location" : string,

&nbsp;&nbsp;"start" : string,

&nbsp;&nbsp;"end" : string,

&nbsp;&nbsp;"description" : string,

&nbsp;&nbsp;"image" : (optional) string

}

**response**:

{}

### POST - /events/delete
##### + Deletes an existing event
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"eid" : int,

}

**response**:

{}


### GET - /courses
##### + Gets all existing bible courses and an existing user's courses
*arguments*:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string

}

*response*:

{

&nbsp;&nbsp;"user_courses": [

&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"member" : [int]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"admin" : [int]

&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;],

&nbsp;&nbsp;"courses": [

&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"cid" : int,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"leader_first" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"leader_last" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"year" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"gender" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"material" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"location" : (optional) string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"day" : (optional) string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"start" : (optional) string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"end" : (optional) string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"groupme" : (optional) string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"abcls" : (optional) [string],

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"members" : [

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"info" : [string],

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"emails" : [string]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"admins" : [

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"emails" : [string]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]

&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;]

}


### POST - /courses/create
##### + Creates a new bible course
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"leader_first" : string,

&nbsp;&nbsp;"leader_last" : string,

&nbsp;&nbsp;"year" : string,

&nbsp;&nbsp;"gender" : string,

&nbsp;&nbsp;"location" : string,

&nbsp;&nbsp;"material" : string,

&nbsp;&nbsp;"meetings" : (optional) {

&nbsp;&nbsp;&nbsp;&nbsp;"day" : string,

&nbsp;&nbsp;&nbsp;&nbsp;"start" : string,

&nbsp;&nbsp;&nbsp;&nbsp;"end" : string

&nbsp;&nbsp;},

&nbsp;&nbsp;"members" : [string],

&nbsp;&nbsp;"admins" : [string]

}

**response**:

{

&nbsp;&nbsp;"cid" : int,

&nbsp;&nbsp;"members" : [int],

&nbsp;&nbsp;"admins" : [int]

}


### POST - /courses/update
##### + Updates an existing bible course
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"cid" : int,

&nbsp;&nbsp;"leader_first" : string,

&nbsp;&nbsp;"leader_last" : string,

&nbsp;&nbsp;"year" : string,

&nbsp;&nbsp;"gender" : string,

&nbsp;&nbsp;"location" : string,

&nbsp;&nbsp;"material" : string,

&nbsp;&nbsp;"meetings" : (optional) {

&nbsp;&nbsp;&nbsp;&nbsp;"day" : string,

&nbsp;&nbsp;&nbsp;&nbsp;"start" : string,

&nbsp;&nbsp;&nbsp;&nbsp;"end" : string

&nbsp;&nbsp;},

&nbsp;&nbsp;"members" : [string],

&nbsp;&nbsp;"admins" : [string]

}

**response**:

{}


### POST - /courses/delete
##### + Deletes an existing bible course
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : int,

&nbsp;&nbsp;"cid" : int

}

**response**:

{}


### POST - /courses/leave
##### + Removes a user from a bible course
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"cid" : int

}


### POST - /courses/request/send
##### + Sends a request for an existing user to join a bible course
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"cid" : int,

&nbsp;&nbsp;"message" : (optional) string

}

**response**:

{}


### GET - /teams
##### + Gets all existing ministry teams and an existing user's ministry teams
*arguments*:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string

}

*response*:

{

&nbsp;&nbsp;"user_teams": [

&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"member" : [int]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"admin" : [int]

&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;],

&nbsp;&nbsp;"teams": [

&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"tid" : int,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"name" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"description" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"leaders" : string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"day" : (optional) string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"start" : (optional) string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"end" : (optional) string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"location" : (optional) string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"groupme" : (optional) string,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"members" : [

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"info" : [string],

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"emails" : [string]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"admins" : [

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"emails" : [string]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]

&nbsp;&nbsp;&nbsp;&nbsp;}

&nbsp;&nbsp;]

}


### POST - /teams/create
##### + Creates a new ministry team
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"name" : string,

&nbsp;&nbsp;"description" : string,

&nbsp;&nbsp;"leaders" : [string],

&nbsp;&nbsp;"members" : [string],

&nbsp;&nbsp;"admins" : [string],

&nbsp;&nbsp;"meetings" : (optional)  {

&nbsp;&nbsp;&nbsp;&nbsp;"day" : string,

&nbsp;&nbsp;&nbsp;&nbsp;"start" : string,

&nbsp;&nbsp;&nbsp;&nbsp;"end" : string,

&nbsp;&nbsp;&nbsp;&nbsp;"location" : string

&nbsp;&nbsp;}

}

**response**:

{

&nbsp;&nbsp;"tid" : int,

&nbsp;&nbsp;"members" : [int],

&nbsp;&nbsp;"admins" : [int]

}


### POST - /teams/update
##### + Updates an existing ministry team
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"tid" : int,

&nbsp;&nbsp;"name" : string,

&nbsp;&nbsp;"description" : string,

&nbsp;&nbsp;"leaders" : [string],

&nbsp;&nbsp;"members" : [string],

&nbsp;&nbsp;"admins" : [string],

&nbsp;&nbsp;"meetings" : (optional)  {

&nbsp;&nbsp;&nbsp;&nbsp;"day" : string,

&nbsp;&nbsp;&nbsp;&nbsp;"start" : string,

&nbsp;&nbsp;&nbsp;&nbsp;"end" : string,

&nbsp;&nbsp;&nbsp;&nbsp;"location" : string

&nbsp;&nbsp;}

}

**response**:

{}


### POST - /teams/delete
##### + Deletes an existing ministry team
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"tid" : int

}

**response**:

{}


### POST - /teams/leave
##### + Removes a user from a ministry team
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"tid" : int

}

**response**:

{}


### POST - /team/request/send
##### + Sends a request for an existing user to join a ministry team
**request**:

{

&nbsp;&nbsp;"uid" : int,

&nbsp;&nbsp;"token" : string,

&nbsp;&nbsp;"tid" : int,

&nbsp;&nbsp;"message" : (optional) string

}

**response**:

{}
