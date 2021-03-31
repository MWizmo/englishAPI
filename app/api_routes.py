# -*- coding: utf-8 -*-
import os
from flask import jsonify, request, Blueprint
from app.models import *
import random


api = Blueprint('api', __name__, template_folder='templates')


def get_word_info(word_id):
    word = Word.query.get(word_id)
    word_info = {'id': word.id, 'enWord': word.en_word, 'ruWord': word.ru_word, 'section': word.section.title,
                 'definition': word.definition, 'partOfSpeech': word.part_of_speech}
    return word_info


@api.route('/modules')
def modules():
    modules_list = []
    for module in Module.query.all():
        modules_list.append({'id': module.id, 'title': module.title})
    return jsonify(modules_list)


@api.route('/modules/<module_id>')
def get_module_info(module_id):
    module = Module.query.get(module_id)
    return jsonify({'id': module.id, 'title': module.title})


@api.route('/sections/<module_id>')
def get_sections(module_id):
    sections = []
    for section in Section.query.filter_by(module_id=module_id).all():
        sections.append({'id': section.id, 'title': section.title})
    return jsonify(sections)


@api.route('/section/<section_id>')
def get_section(section_id):
    section = Section.query.get(section_id)
    return jsonify({'id': section.id, 'title': section.title})


@api.route('/user_words/<user_id>')
def get_words_of_user(user_id):
    words = []
    for word in Dictionary.query.filter_by(user_id=user_id).all():
        words.append(get_word_info(word.word.id))
    return jsonify(words)


@api.route('/words/<section_id>')
def get_words_of_section(section_id):
    words = []
    for word in Word.query.filter_by(section_id=section_id).all():
        words.append(get_word_info(word.id))
    return jsonify(words)


@api.route('/word/<word_id>')
def get_word_by_id(word_id):
    return jsonify(get_word_info(word_id))


@api.route('/tasks/<section_id>')
def get_tasks_of_section(section_id):
    tasks = TaskInSection.query.filter_by(section_id=section_id).all()
    tasks_info = []
    for t in tasks:
        tasks_info.append({'type': t.task_type, 'taskId': t.task_id, 'id': t.id, 'sectionId': t.section_id})
    return jsonify(tasks_info)


@api.route('/task/<task_id>')
def get_tasks_info(task_id):
    t = TaskInSection.query.get(task_id)
    return jsonify({'type': t.task_type, 'taskId': t.task_id, 'id': t.id, 'sectionId': t.section_id})


@api.route('/en_translation_task/<section_id>')
def get_words_from_section(section_id):
    words = Word.query.filter_by(section_id=section_id).all()
    random.shuffle(words)
    rand_index = random.randint(0, 3)
    task = []
    for i in range(4):
        task.append({'enWord': words[i].en_word, 'ruWord': words[i].ru_word, 'isRight': i == rand_index})
    return jsonify(task)


@api.route('/add_to_dictionary', methods=['POST'])
def add_to_dictionary():
    r = request.json
    new_row = Dictionary(user_id=r['userId'], word_id=r['wordId'])
    db.session.add(new_row)
    db.session.commit()
    word = Word.query.get(r['wordId'])
    return jsonify({"status": 200, "message": word.en_word})

