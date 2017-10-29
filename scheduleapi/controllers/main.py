from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser
from flask import jsonify, abort, request, json, g
from flask_httpauth import HTTPBasicAuth as Auth
from flask_security import Security, MongoEngineUserDatastore
from flask import current_app as app

from scheduleapi.extensions import cache
from scheduleapi.forms import LoginForm
from scheduleapi.models import User, db
import datetime

main = Blueprint('main', __name__)
auth = Auth(app)


@auth.verify_password
def verify_password(email_or_token, password):
    user = User.verify_auth_token(email_or_token)
    if not user:
        # attempt to auth with email/password
        user = User.objects(email=email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


class RegisterResource(Resource):
    def post(self):
        user_datastore = app.user_datastore
        email = request.json.get("email")
        password = request.json.get("password")
        if not email or not password:
            abort(400)
        if User.objects(email=email).first():
            abort(400)
        user = User()
        user.email = email
        user.set_password(password)
        user_datastore.create_user(
                password_hash=user.password_hash,
                email=user.email,
                roles=["admin"],
                confirmed_at=datetime.datetime.now())
        return {"email": user.email}, 201


class RestrictedUsersResource(Resource):
    decorators = [auth.login_required]

    def get(self):
        return {"message": "You authenticated properly"}


class TokenResource(Resource):
    decorators = [auth.login_required]
    def get(self):
        token = g.user.generate_auth_token()
        print("TOKEN: {}".format(token))
        return {"token": token.decode("ascii")}
