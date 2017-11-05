from flask_mongoengine import MongoEngine
from flask import current_app as app
from flask_security import Security, MongoEngineUserDatastore, UserMixin
from flask_security import utils, core, RoleMixin
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired, BadData)

db = MongoEngine()



class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    f_name = db.StringField()
    l_name = db.StringField()
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    password_hash = db.StringField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    email = db.StringField(unique=True)

    def set_password(self, password_hash):
        self.password_hash = utils.hash_password(password_hash)

    def verify_password(self, value):
        return utils.verify_password(value, self.password_hash)

    def generate_auth_token(self, expiration=15000):
        s = Serializer(app.config["SECRET_KEY"], expires_in=expiration)
        token = s.dumps({'email': self.email})
        return token

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        data = None
        try:
            data = s.loads(token)
        except SignatureExpired:
            print("Signature Expired")
            return None
        except BadSignature:
            print("Signature is bad")
            return None
        user = User.objects(email=data["email"]).first()
        return user

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class Jobs(db.Document):
    clientname = db.StringField()
    address = db.StringField()
    contact_number = db.StringField()
    details = db.StringField()
    keywords = db.StringField()
    employee = db.ReferenceField(User)
