from flask_admin.contrib.sqlamodel import ModelView
from flask import request, redirect, url_for, render_template
from flask_login import current_user
from flask_admin import AdminIndexView, expose
from wtforms.validators import DataRequired
from wtforms import SelectField, TextAreaField
from app.models import Section


class IndexView(AdminIndexView):
    def is_visible(self):
        return False

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.url))
        return redirect(url_for('module.index_view'))

    @expose('/tasks/')
    def tasks(self):
        sections = Section.query.all()
        return render_template('/tasks_view.html', sections=sections)


class MyView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class ModuleView(MyView):
    form_args = {
        'title': {
            'label': 'Title',
            'validators': [DataRequired()]
        }
    }


class SectionView(MyView):
    form_args = {
        'title': {
            'label': 'Title',
            'validators': [DataRequired()]
        },
        'module': {
            'label': 'Module',
            'validators': [DataRequired()]
        }
    }
    column_list = ['title', 'module.title']
    column_labels = {'title': 'Title', 'module.title': 'Module'}
    column_sortable_list = ['module.title']


class WordView(MyView):
    form_args = {
        'en_word': {'label': 'Word in English', 'validators': [DataRequired()]},
        'ru_word': {'label': 'Word in Russian', 'validators': [DataRequired()]},
        'section': {'label': 'Section', 'validators': [DataRequired()]}
    }
    form_extra_fields = {'part_of_speech': SelectField('Part of speech', choices=[('Noun', 'Noun'), ('Verb', 'Verb'),
                                                                                  ('Adjective', 'Adjective'),
                                                                                  ('Pronoun', 'Pronoun'),
                                                                                  ('Adverb', 'Adverb')],
                                                       validators=[DataRequired()]),
                         'definition': TextAreaField('Definition', validators=[DataRequired()])}
    column_list = ['en_word', 'ru_word', 'part_of_speech', 'definition', 'section.title']
    column_labels = {'en_word': 'In English', 'ru_word': 'In Russian', 'part_of_speech': 'Part of speech',
                     'definition': 'Definition', 'section.title': 'Section'}
    column_sortable_list = ['section.title', 'en_word', 'ru_word', 'part_of_speech']
    column_searchable_list = ['en_word', 'ru_word']
    column_default_sort = ('en_word', False)


class TasksView(MyView):
    list_template = 'tasks_view.html'
