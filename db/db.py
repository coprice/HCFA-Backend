import psycopg2 as psg
import hashlib, secrets

from config.config import Config


class DB:
    def __init__(self):
        self.config = Config()
        connect_str = "dbname='%s' user='%s' host='%s' password='%s'" % (
            self.config.dbName, self.config.dbUser, self.config.dbURI, self.config.dbPassword
        )
        conn = psg.connect(connect_str)
        conn.autocommit = True
        self.db = conn.cursor()

    def register_user(self, first_name, last_name, email, password):

        self.db.execute("""
                SELECT uid FROM users WHERE email = %s
            """,
            (email,))
        exists = self.db.fetchone()

        if exists:
            return {'error': 'User already exists', 'status': 409}

        pass_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
        token = secrets.token_hex()

        self.db.execute("""
                INSERT INTO users (first_name, last_name, email, pass, token)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING uid, admin, leader
            """,
            (first_name, last_name, email, pass_hash, token))

        row = self.db.fetchone()
        if row is None:
            return {'error': 'Unable to create user', 'status': 500}

        uid, admin, leader  = row

        return {
            'uid': uid,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'admin': admin,
            'leader': leader,
            'token': token,
        }

    def login_user(self, email, password):

        pass_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()

        self.db.execute("""
                SELECT uid, first_name, last_name, admin, leader, profile
                FROM users
                WHERE email = %s AND pass = %s
            """,
            (email, pass_hash))

        row = self.db.fetchone()
        if row is None:
            return {'error': 'Invalid email or password', 'status': 401}

        uid, first_name, last_name, admin, leader, profile = row

        token = secrets.token_hex()
        self.db.execute("""
                UPDATE users SET token = %s WHERE uid = %s
            """,
            (token, uid))

        return {
            'uid': uid,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'admin': admin,
            'leader': leader,
            'token': token,
            'image': profile
        }

    def validate_session(self, uid, token):
        self.db.execute("""
                SELECT uid FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        if self.db.fetchone() is None:
            return {'error': 'Session Expired', 'status': 403}

        return {'validated': True}

    def change_permission(self, uid, token, email, perm='leader', is_add=True):

        self.db.execute("""
                SELECT admin FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        row = self.db.fetchone()
        if row is None or not row[0]:
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                SELECT {} FROM users WHERE email = %s
            """.format(perm),
            (email,))

        row = self.db.fetchone()
        if row is None:
            return {'error': 'User does not exist', 'status': 409}

        (target_perm,) = row

        if is_add == target_perm:

            a_an = 'a'
            if not is_add:
                a_an = 'not a'

            if perm == 'admin':
                a_an += 'n'

            return {'error': 'User is already {a_an} {perm}'.format(
                        a_an=a_an, perm=perm),
                    'status': 409}

        token = secrets.token_hex()

        self.db.execute("""
                UPDATE users SET {perm} = {is_add}, token = %s WHERE email = %s
            """.format(perm=perm, is_add=is_add),
            (token, email))

        return {}

    def change_password(self, uid, token, old_password, new_password):

        self.db.execute("""
                SELECT uid FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        if self.db.fetchone() is None:
            return {'error': 'Session Expired', 'status': 403}

        old_hash = hashlib.sha1(old_password.encode('utf-8')).hexdigest()

        self.db.execute("""
                SELECT uid FROM users WHERE uid = %s AND pass = %s
            """,
            (uid, old_hash))

        if self.db.fetchone() is None:
            return {'error': 'Invalid password', 'status': 401}

        pass_hash = hashlib.sha1(new_password.encode('utf-8')).hexdigest()

        self.db.execute("""
                UPDATE users SET pass = %s WHERE uid = %s
            """,
            (pass_hash, uid))

        return {}

    def update_contact(self, uid, token, first, last, email):

        self.db.execute("""
                SELECT uid FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        if self.db.fetchone() is None:
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                UPDATE users SET first_name = %s, last_name = %s, email = %s
                WHERE uid = %s
            """,
            (first, last, email, uid))

        return {}

    def update_image(self, uid, token, image):

        self.db.execute("""
                SELECT uid FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        if self.db.fetchone() is None:
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                UPDATE users SET profile = %s WHERE uid = %s
            """,
            (image, uid))

        return {}

    def get_events(self):

        self.db.execute("""
                SELECT * FROM events
                WHERE current_timestamp < TO_TIMESTAMP(end_date, 'YYYY-MM-DD HH24:MI:SS')
                ORDER BY TO_TIMESTAMP(start_date, 'YYYY-MM-DD HH24:MI:SS')
            """)

        upcoming_rows = map(lambda x: {'eid': x[0], 'title': x[1],
                            'location': x[2], 'start': x[3],
                            'end': x[4], 'description': x[5],'image': x[6]},
                            self.db.fetchall())

        self.db.execute("""
                SELECT * FROM events
                WHERE current_timestamp > TO_TIMESTAMP(end_date, 'YYYY-MM-DD HH24:MI:SS')
                ORDER BY TO_TIMESTAMP(start_date, 'YYYY-MM-DD HH24:MI:SS') DESC
            """)

        past_rows = map(lambda x: {'eid': x[0], 'title': x[1], 'location': x[2],
                                   'start': x[3], 'end': x[4],
                                   'description': x[5],'image': x[6]},
                            self.db.fetchall())

        return {
            'upcoming_events': upcoming_rows,
            'past_events': past_rows
        }

    def create_event(self, uid, token, title, location, start, end, description, image):

        self.db.execute("""
                SELECT admin, leader FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        row = self.db.fetchone()
        if row is None or not (row[0] or row[1]):
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                INSERT INTO events (title, event_location, start_date, end_date, description, image)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING eid
            """,
            (title, location, start, end, description, image))

        row = self.db.fetchone()
        if row is None:
            return {'error': 'Unable to create event', 'status': 500}

        (eid,) = row

        return {
            'eid': eid,
        }

    def update_event(self, uid, token, eid, title, location, start, end,
                     description, image):

        self.db.execute("""
                SELECT admin, leader FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        row = self.db.fetchone()
        if row is None or not (row[0] or row[1]):
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                UPDATE events SET title = %s, event_location = %s, start_date = %s,
                                                    end_date = %s, description = %s, image = %s
                WHERE eid = %s
                RETURNING eid
            """,
            (title, location, start, end, description, image, eid))

        if self.db.fetchone() is None:
            return {'error': 'Event does not exist', 'status': 409}

        return {}

    def delete_events(self, uid, token, events):

        self.db.execute("""
                SELECT admin, leader FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        row = self.db.fetchone()
        if row is None or not (row[0] or row[1]) or \
            (not row[0] and len(events) > 1):
            return {'error': 'Session Expired', 'status': 403}

        for eid in events:
            self.db.execute("""
                    DELETE FROM events WHERE eid = %s
                """,
                (eid,))

        return {}

    def get_courses(self, uid, token):

        self.db.execute("""
                SELECT uid FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        if self.db.fetchone() is None:
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                SELECT cid, is_admin FROM course_members WHERE uid = %s
            """,
            (uid,))

        user_member, user_admin = [], []
        for cid, is_admin in self.db.fetchall():
            if is_admin:
                user_admin.append(cid)
            else:
                user_member.append(cid)
        user_courses = {'member': user_member, 'admin': user_admin}

        self.db.execute("""
                SELECT cid, leader_first, leader_last, course_year, gender,
                       course_location, material, course_day, start_time,
                       end_time, abcls, groupme
                FROM courses
            """)
        courses = self.db.fetchall()

        self.db.execute("""
                SELECT cid, first_name, last_name, email, is_admin FROM
                course_members JOIN users ON course_members.uid = users.uid
            """)

        users = self.db.fetchall()

        return {
            'user_courses': user_courses,
            'courses': map(lambda course: self.format_course(course, users), courses)
        }

    def create_course(self, uid, token, leader_first, leader_last, year,
                      gender, location, material, meetings,
                      abcls, groupme, members, admins):

        self.db.execute("""
                SELECT admin FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        row = self.db.fetchone()
        if row is None or not row[0]:
            return {'error': 'Session Expired', 'status': 403}

        ids = self.get_user_ids(members, admins)
        if ids[0] is None:
            return {'error': 'User not found: {}'.format(ids[1]), 'status': 404}
        member_ids, admin_ids = ids

        abcl_names = '|'.join(abcls)

        if meetings:
            self.db.execute("""
                    INSERT INTO courses
                        (leader_first, leader_last, course_year, gender,
                         course_location, material, course_day, start_time,
                         end_time, abcls, groupme)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING cid
                """,
                (leader_first, leader_last, year, gender,
                 location, material, meetings['day'], meetings['start'],
                 meetings['end'], abcl_names, groupme))
        else:
            self.db.execute("""
                    INSERT INTO courses
                        (leader_first, leader_last, course_year, gender,
                         course_location, material, abcls, groupme)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING cid
                """,
                (leader_first, leader_last, year, gender,
                 location, material, abcl_names, groupme))

        row = self.db.fetchone()
        if row is None:
            return {'error': 'Unable to create bible course', 'status': 500}

        (cid,) = row

        for uid in member_ids:
            self.db.execute("""
                    INSERT INTO course_members (uid, cid)
                    VALUES (%s, %s)
                """,
                (uid, cid))

        for uid in admin_ids:
            self.db.execute("""
                    INSERT INTO course_members (uid, cid, is_admin)
                    VALUES (%s, %s, TRUE)
                """,
                (uid, cid))

        return {
            'cid': cid,
        }

    def update_course(self, uid, token, cid, leader_first, leader_last,
                      year, gender, location, material, meetings,
                      abcls, groupme, members, admins):

        self.db.execute("""
                SELECT uid FROM course_members WHERE cid = %s AND is_admin = TRUE
            """,
            (cid,))
        current_admins = map(lambda x: x[0], self.db.fetchall())

        self.db.execute("""
                SELECT admin FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        row = self.db.fetchone()
        if row is None or not (row[0] or uid in current_admins):
            return {'error': 'Session Expired', 'status': 403}

        ids = self.get_user_ids(members, admins)
        if ids[0] is None:
            return {'error': 'User not found: {}'.format(ids[1]), 'status': 404}
        member_ids, admin_ids = ids

        abcl_names = '|'.join(abcls)

        if meetings:
            self.db.execute("""
                    UPDATE courses
                    SET leader_first = %s, leader_last = %s, course_year = %s,
                        gender = %s, course_location = %s, material = %s,
                        course_day = %s, start_time = %s, end_time = %s,
                        abcls = %s, groupme = %s
                    WHERE cid = %s
                    RETURNING cid
                """,
                (leader_first, leader_last, year, gender, location, material,
                 meetings['day'], meetings['start'], meetings['end'],
                 abcl_names, groupme, cid))
        else:
            self.db.execute("""
                    UPDATE courses
                    SET leader_first = %s, leader_last = %s, course_year = %s,
                        gender = %s, course_location = %s, material = %s,
                        course_day = null, start_time = null, end_time = null,
                        abcls = %s, groupme = %s
                    WHERE cid = %s
                    RETURNING cid
                """,
                (leader_first, leader_last, year, gender, location,
                 material, abcl_names, groupme, cid))

        if self.db.fetchone() is None:
            return {'error': 'Course does not exist', 'status': 409}

        self.db.execute("""
                DELETE FROM course_members WHERE cid = %s
            """,
            (cid,))

        for uid in member_ids:
            self.db.execute("""
                    INSERT INTO course_members (uid, cid)
                    VALUES (%s, %s)
                """,
                (uid, cid))

        for uid in admin_ids:
            self.db.execute("""
                    INSERT INTO course_members (uid, cid, is_admin)
                    VALUES (%s, %s, TRUE)
                """,
                (uid, cid))

        return {}

    def delete_course(self, uid, token, cid):

        self.db.execute("""
                SELECT uid FROM course_members WHERE cid = %s AND is_admin = TRUE
            """,
            (cid,))
        admins = self.db.fetchall()

        self.db.execute("""
                SELECT admin FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        row = self.db.fetchone()
        if row is None or not (row[0] or uid in admins):
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                DELETE FROM course_members WHERE cid = %s
            """,
            (cid,))

        self.db.execute("""
                DELETE FROM courses WHERE cid = %s
            """,
            (cid,))

        return {}

    def leave_course(self, uid, token, cid):

        self.db.execute("""
                SELECT uid FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        if self.db.fetchone() is None:
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                DELETE FROM course_members WHERE uid = %s AND cid = %s
            """,
            (uid, cid))

        return {}

    def prepare_course_request(self, uid, token, cid):

        self.db.execute("""
                SELECT first_name, last_name, email FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        user = self.db.fetchone()
        if user is None:
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                SELECT first_name, last_name, email FROM
                course_members JOIN users
                ON course_members.uid = users.uid AND cid = %s AND is_admin = TRUE
            """,
            (cid,))

        return {
            'user': ('{} {}'.format(user[0], user[1]), user[2]),
            'admins': map(lambda x: ('{} {}'.format(x[0], x[1]), x[2]), self.db.fetchall())
        }

    def complete_course_request(self, uid, cid, email, password):

        pass_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()

        self.db.execute("""
                SELECT admin, uid FROM users WHERE email = %s AND pass = %s
            """,
            (email, pass_hash))

        user = self.db.fetchone()

        if user is None:
            return {'error': 'Invalid email or password'}

        (admin, admin_uid) = user

        self.db.execute("""
                SELECT is_admin FROM course_members WHERE uid = %s AND cid = %s
            """,
            (admin_uid, cid))

        res = self.db.fetchone()

        if res is None and not admin or (res is not None and not (res[0] or admin)):
            return {'error': 'You are not an admin for this course'}

        self.db.execute("""
                SELECT uid FROM course_members WHERE uid = %s AND cid = %s
            """,
            (uid, cid))

        if not self.db.fetchone() is None:
            return {'error': 'User already is in this course'}

        self.db.execute("""
                INSERT INTO course_members (uid, cid) VALUES (%s, %s)
            """,
            (uid, cid))

        return {}

    def get_teams(self, uid, token):

        self.db.execute("""
                SELECT uid FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        if self.db.fetchone() is None:
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                SELECT tid, is_admin FROM team_members WHERE uid = %s
            """,
            (uid,))

        user_member, user_admin = [], []
        for tid, is_admin in self.db.fetchall():
            if is_admin:
                user_admin.append(tid)
            else:
                user_member.append(tid)
        user_teams = {'member': user_member, 'admin': user_admin}

        self.db.execute("""
                SELECT tid, name, description, leaders, meeting_day,
                       meeting_start, meeting_end, meeting_location, groupme
                FROM teams
            """)
        teams = self.db.fetchall()

        self.db.execute("""
                SELECT tid, first_name, last_name, email, is_admin FROM
                team_members JOIN users ON team_members.uid = users.uid
            """)
        users = self.db.fetchall()

        return {
            'user_teams': user_teams,
            'teams': map(lambda team: self.format_team(team, users), teams)
        }

    def create_team(self, uid, token, name, description, leaders, meetings,
                    groupme, members, admins):

        self.db.execute("""
                SELECT admin FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        row = self.db.fetchone()
        if row is None or not row[0]:
            return {'error': 'Session Expired', 'status': 403}

        ids = self.get_user_ids(members, admins)
        if ids[0] is None:
            return {'error': 'User not found: {}'.format(ids[1]), 'status': 404}
        member_ids, admin_ids = ids

        leader_names = '|'.join(leaders)

        if meetings:
            self.db.execute("""
                    INSERT INTO teams
                        (name, description, leaders, meeting_day, meeting_start,
                         meeting_end, meeting_location, groupme)
                    VALUES
                        (%s, %s, %s, %s, %s, %s , %s, %s)
                    RETURNING tid
                """,
                (name, description, leader_names, meetings['day'],
                 meetings['start'], meetings['end'],
                 meetings['location'], groupme))

        else:
            self.db.execute("""
                    INSERT INTO teams (name, description, leaders, groupme)
                    VALUES (%s, %s, %s, %s)
                    RETURNING tid
                """,
                (name, description, leader_names, groupme))

        row = self.db.fetchone()
        if row is None:
            return {'error': 'Unable to create ministry team', 'status': 500}

        (tid,) = row

        for uid in member_ids:
            self.db.execute("""
                    INSERT INTO team_members (uid, tid)
                    VALUES (%s, %s)
                """,
                (uid, tid))

        for uid in admin_ids:
            self.db.execute("""
                    INSERT INTO team_members (uid, tid, is_admin)
                    VALUES (%s, %s, TRUE)
                """,
                (uid, tid))

        return {
            'tid': tid,
        }

    def update_team(self, uid, token, tid, name, description, leaders,
                   meetings, groupme, members, admins):

        self.db.execute("""
                SELECT uid FROM team_members WHERE tid = %s AND is_admin = TRUE
            """,
            (tid,))
        current_admins = map(lambda x: x[0], self.db.fetchall())

        self.db.execute("""
                SELECT admin FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        row = self.db.fetchone()
        if row is None or not (row[0] or uid in current_admins):
            return {'error': 'Session Expired', 'status': 403}

        ids = self.get_user_ids(members, admins)
        if ids[0] is None:
            return {'error': 'User not found: {}'.format(ids[1]), 'status': 404}
        member_ids, admin_ids = ids

        leader_names = '|'.join(leaders)

        if meetings:
            self.db.execute("""
                    UPDATE teams
                    SET name = %s, description = %s, leaders = %s,
                        meeting_day = %s, meeting_start = %s, meeting_end = %s,
                        meeting_location = %s, groupme = %s
                    WHERE tid = %s
                    RETURNING tid
                """,
                (name, description, leader_names, meetings['day'],
                 meetings['start'], meetings['end'], meetings['location'],
                 groupme, tid))

        else:
            self.db.execute("""
                    UPDATE teams
                    SET name = %s, description = %s, leaders = %s,
                        meeting_day = null, meeting_start = null,
                        meeting_end = null, meeting_location = null,
                        groupme = %s
                    WHERE tid = %s
                    RETURNING tid
                """,
                (name, description, leader_names, groupme, tid))

        if self.db.fetchone() is None:
            return {'error': 'Team does not exist', 'status': 409}

        self.db.execute("""
                DELETE FROM team_members WHERE tid = %s
            """,
            (tid,))

        for uid in member_ids:
            self.db.execute("""
                    INSERT INTO team_members (uid, tid)
                    VALUES (%s, %s)
                """,
                (uid, tid))

        for uid in admin_ids:
            self.db.execute("""
                    INSERT INTO team_members (uid, tid, is_admin)
                    VALUES (%s, %s, TRUE)
                """,
                (uid, tid))

        return {}

    def delete_team(self, uid, token, tid):

        self.db.execute("""
                SELECT uid FROM team_members WHERE tid = %s AND is_admin = TRUE
            """,
            (tid,))
        admins = self.db.fetchall()

        self.db.execute("""
                SELECT admin FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        row = self.db.fetchone()
        if row is None or not (row[0] or uid in admins):
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                DELETE FROM team_members WHERE tid = %s
            """,
            (tid,))

        self.db.execute("""
                DELETE FROM teams WHERE tid = %s
            """,
            (tid,))

        return {}

    def leave_team(self, uid, token, tid):

        self.db.execute("""
                SELECT uid FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        if self.db.fetchone() is None:
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                DELETE FROM team_members WHERE uid = %s AND tid = %s
            """,
            (uid, tid))

        return {}

    def prepare_team_request(self, uid, token, tid):

        self.db.execute("""
                SELECT first_name, last_name, email FROM users WHERE uid = %s AND token = %s
            """,
            (uid, token))

        user = self.db.fetchone()
        if user is None:
            return {'error': 'Session Expired', 'status': 403}

        self.db.execute("""
                SELECT first_name, last_name, email FROM
                team_members JOIN users ON team_members.uid = users.uid
                    AND tid = %s AND is_admin = TRUE
            """,
            (tid,))

        return {
            'user': ('{} {}'.format(user[0], user[1]), user[2]),
            'admins': map(lambda x: ('{} {}'.format(x[0], x[1]), x[2]), self.db.fetchall())
        }

    def get_users_info(self, uid):

        self.db.execute("""
                SELECT first_name, last_name, email FROM users WHERE uid = %s
            """,
            (uid,))

        return self.db.fetchone()

    def get_course_info(self, cid):

        self.db.execute("""
                SELECT leader_first, course_year, gender
                FROM courses WHERE cid = %s
            """,
            (cid,))

        return self.db.fetchone()

    def get_team_info(self, tid):

        self.db.execute("""
                SELECT name FROM teams WHERE tid = %s
            """,
            (tid,))

        return self.db.fetchone()



    ### HELPERS ###

    def get_user_ids(self, members, admins):
        member_ids = []
        for email in members:
            self.db.execute("""
                    SELECT uid FROM users WHERE email = %s
                """,
                (email,))

            row = self.db.fetchone()
            if row is None:
                return (None, email)

            (uid,) = row
            member_ids.append(uid)

        admin_ids = []
        for email in admins:
            self.db.execute("""
                    SELECT uid FROM users WHERE email = %s
                """,
                (email,))

            row = self.db.fetchone()
            if row is None:
                return (None, email)

            (uid,) = row
            admin_ids.append(uid)
        return member_ids, admin_ids

    def extract_user_info(self, uid, users):

        member_names, member_emails = [], []
        for user in filter(lambda user: user[0] == uid and not user[4], users):
            member_names.append('{} {}'.format(user[1], user[2]))
            member_emails.append(user[3])

        admin_emails = []
        for user in filter(lambda user: user[0] == uid and user[4], users):
            admin_emails.append(user[3])

        return ({'names': member_names, 'emails': member_emails},
                {'emails': admin_emails})

    def format_team(self, team, users):

        members, admins = self.extract_user_info(team[0], users)

        leaders = team[3].split('|')
        if team[3] == '':
            leaders = []

        return {
            'tid': team[0], 'name': team[1], 'description': team[2],
            'leaders': leaders, 'day': team[4], 'start': team[5],
            'end': team[6], 'location': team[7], 'groupme': team[8],
            'members': members, 'admins': admins
        }

    def format_course(self, course, users):

        members, admins = self.extract_user_info(course[0], users)

        abcls = course[10].split('|')
        if course[10] == '':
            abcls = []

        return {
            'cid': course[0], 'leader_first': course[1],
            'leader_last': course[2], 'year': course[3], 'gender': course[4],
            'location': course[5], 'material': course[6], 'day': course[7],
            'start': course[8], 'end': course[9], 'groupme': course[11],
            'abcls': abcls, 'members': members, 'admins': admins,
        }

db = DB()
