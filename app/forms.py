# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm = PasswordField("Repeat password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")])


class AddModuleForm(FlaskForm):
    title = StringField("Module's title", validators=[DataRequired()])


class AddSectionForm(FlaskForm):
    title = StringField("Theme's title", validators=[DataRequired()])
    module = StringField("Module", validators=[DataRequired()])


class AddWordForm(FlaskForm):
    en_word = StringField("Word in English", validators=[DataRequired()])
    ru_word = StringField("Word in Russian", validators=[DataRequired()])
    part_of_speech = StringField("Part of speech", validators=[DataRequired()])
    section = StringField("Section", validators=[DataRequired()])
    definition = StringField("Definition", validators=[DataRequired()])
