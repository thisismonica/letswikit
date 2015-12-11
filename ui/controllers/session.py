__author__ = 'suparngupta'

import hashlib

from flask import request, g, abort
import rethinkdb as r

import helpers.auth as auth
from app import app
from models.Error import *


@app.route("/session/login/", methods=['POST'])
def login_user():
    body = request.get_json()
    print(body)
    if "username" not in body or "password" not in body:
        abort(400)
    hash_user = hashlib.md5(body['username'].encode('utf-8')).hexdigest()
    auth_token = auth.generate_auth_token()

    result = r.table('user').get(hash_user).run(g.rdb_conn)
    if result is None:
        print("bad_username")
        raise NotFound(message="incorrect_username")
    if result['password'] != auth.generate_password_hash(body['password']):
        print("bad_password")
        raise NotFound(message="incorrect_username")

    else:
        user_token = r.table('user_token').insert({
            'user_id': hash_user,
            'auth_token': auth_token,
        }).run(g.rdb_conn)
        if user_token['errors'] == 0:
            return jsonify({'user_id': hash_user, 'auth_token': auth_token})
        else:
            print("unable_to_create_session_token")
            raise InternalServerError(message="unable_to_create_session")


@app.route("/session/signup/", methods=['POST'])
def create_user():
    body = request.get_json()
    if "username" not in body or "password" not in body:
        raise BadRequest(message="username_or_password_missing")

    hash_user = hashlib.md5(body['username'].encode('utf-8')).hexdigest()
    auth_token = auth.generate_auth_token()
    user = r.table('user').insert({
        'id': hash_user,
        'username': body['username'],
        'password': auth.generate_password_hash(body['password']),
        'created_at': r.now()
    }).run(g.rdb_conn)

    if user['errors'] == 0:
        user_token = r.table('user_token').insert({
            'user_id': hash_user,
            'auth_token': auth_token,
        }).run(g.rdb_conn)

        if user_token['errors'] == 0:
            return jsonify({'user_id': hash_user, 'auth_token': auth_token})
        else:
            print("unable_to_create_session_token_try_logging_in")
            raise InternalServerError()
    else:
        raise InternalServerError()


@app.route("/session/logout/", methods=['POST'])
def logout_user():
    body = request.get_json()
    if "user_id" not in body or "auth_token" not in body:
        raise BadRequest(message="missing_user_id_or_auth_token")

    data_deleted = r.table("user_token").filter({"user_id": body['user_id'],
                                                 "auth_token": body['auth_token']}).delete().run(g.rdb_conn)
    if data_deleted['deleted'] == 1:
        return jsonify(status="okay")
    else:
        raise NotFound(message="auth_token_not_found")


def load():
    pass
