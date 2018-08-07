CREATE TABLE users(uid SERIAL PRIMARY KEY,
                   first_name VARCHAR NOT NULL,
                   last_name VARCHAR NOT NULL,
                   email VARCHAR NOT NULL,
                   pass VARCHAR NOT NULL,
                   admin BOOLEAN DEFAULT FALSE,
                   leader BOOLEAN DEFAULT FALSE,
                   token VARCHAR,
                   profile VARCHAR)

CREATE TABLE events(eid SERIAL PRIMARY KEY,
                    title VARCHAR NOT NULL,
                    event_location VARCHAR NOT NULL,
                    start_date VARCHAR NOT NULL,
                    end_date VARCHAR NOT NULL,
                    description VARCHAR NOT NULL,
                    image VARCHAR)

CREATE TABLE courses(cid SERIAL PRIMARY KEY,
                     leader_first VARCHAR NOT NULL,
                     leader_last VARCHAR NOT NULL,
                     course_year VARCHAR NOT NULL,
                     gender VARCHAR NOT NULL,
                     course_location VARCHAR NOT NULL,
                     material VARCHAR NOT NULL,
                     course_day VARCHAR,
                     start_time VARCHAR,
                     end_time VARCHAR,
                     abcls VARCHAR,
                     groupme VARCHAR)

CREATE TABLE teams(tid SERIAL PRIMARY KEY,
                   name VARCHAR NOT NULL,
                   description VARCHAR NOT NULL,
                   leaders VARCHAR NOT NULL,
                   meeting_day VARCHAR,
                   meeting_start VARCHAR,
                   meeting_end VARCHAR,
                   meeting_location VARCHAR,
                   groupme VARCHAR)

CREATE TABLE course_members(uid INTEGER NOT NULL,
                            cid INTEGER NOT NULL,
                            is_admin BOOLEAN DEFAULT FALSE)

CREATE TABLE team_members(uid INTEGER NOT NULL,
                          tid INTEGER NOT NULL,
                          is_admin BOOLEAN DEFAULT FALSE)

CREATE TABLE team_requests(uid INTEGER NOT NULL,
                           cid INTEGER NOT NULL,
                           token VARCHAR NOT NULL)

CREATE TABLE course_requests(uid INTEGER NOT NULL,
                             tid INTEGER NOT NULL,
                             token VARCHAR NOT NULL)

CREATE TABLE password_requests(uid INTEGER NOT NULL,
                               token VARCHAR NOT NULL)
