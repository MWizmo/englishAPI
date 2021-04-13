from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


ROLE_USER = 0
ROLE_ADMIN = 1


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    first_name = db.Column(db.String(30), default='')
    last_name = db.Column(db.String(30), default='')
    role = db.Column(db.Integer, default=ROLE_USER)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN

    @staticmethod
    def get_by_id(uid):
        return User.query.filter_by(id=uid).first()


class Module(db.Model):
    __tablename__ = "module"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))

    def __repr__(self):
        return self.title


class Section(db.Model):
    __tablename__ = "section"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    module = db.relationship("Module")

    def __repr__(self):
        return self.title


class Word(db.Model):
    __tablename__ = "word"
    id = db.Column(db.Integer, primary_key=True)
    en_word = db.Column(db.String(64))
    ru_word = db.Column(db.String(64))
    part_of_speech = db.Column(db.String(32))
    definition = db.Column(db.String(256))
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    section = db.relationship("Section")

    def __repr__(self):
        return self.en_word


class TaskInSection(db.Model):
    __tablename__ = "task_in_section"
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    section = db.relationship("Section")
    task_type = db.Column(db.Integer)
    task_id = db.Column(db.Integer)


class Dictionary(db.Model):
    __tablename__ = "dictionary"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    word = db.relationship("Word")


class UserStat(db.Model):
    __tablename__ = 'user_stat'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    word = db.relationship("Word")
    correct_attempts = db.Column(db.Integer)
    wrong_attempts = db.Column(db.Integer)
    last_try_time = db.Column(db.DateTime)
