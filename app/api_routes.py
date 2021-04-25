# -*- coding: utf-8 -*-
import os
from flask import jsonify, request, Blueprint
from app.models import *
import random
from datetime import datetime as dt

api = Blueprint('api', __name__, template_folder='templates')


def get_current_date():
    return dt(dt.now().year, dt.now().month, dt.now().day, dt.now().hour, dt.now().minute)


def get_word_info(word_id, user_id=0):
    word = Word.query.get(word_id)
    if user_id == 0:
        inDictionary = False
    else:
        word_query = Dictionary.query.filter(Dictionary.word_id == word_id, Dictionary.user_id == user_id).first()
        inDictionary = word_query is not None
    word_info = {'id': word.id, 'enWord': word.en_word, 'ruWord': word.ru_word, 'section': word.section.title,
                 'definition': word.definition, 'partOfSpeech': word.part_of_speech, 'inDictionary': inDictionary,
                 'sectionId': word.section.id}
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


@api.route('/word/<word_id>&<user_id>')
def get_word_by_id(word_id, user_id):
    return jsonify(get_word_info(word_id, user_id))


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


@api.route('/translation_task/<section_id>&<previous_word_id>')
def get_words_from_section(section_id, previous_word_id):
    words = Word.query.filter_by(section_id=section_id).all()
    random.shuffle(words)
    rand_index = random.randint(0, 3)
    while words[rand_index].id == previous_word_id:
        random.shuffle(words)
        rand_index = random.randint(0, 3)
    task = []
    for i in range(4):
        task.append({'enWord': words[i].en_word, 'ruWord': words[i].ru_word, 'isRight': i == rand_index, 'wordId': words[i].id})
    return jsonify(task)


@api.route('/add_to_dictionary', methods=['POST'])
def add_to_dictionary():
    req = request.json
    new_row = Dictionary(user_id=req['userId'], word_id=req['wordId'])
    db.session.add(new_row)
    db.session.commit()
    word = Word.query.get(req['wordId'])
    return jsonify({"status": 200, "message": word.en_word})


@api.route('/remove_from_dictionary', methods=['POST'])
def remove_from_dictionary():
    req = request.json
    Dictionary.query.filter(Dictionary.user_id == req['userId'], Dictionary.word_id == req['wordId']).delete()
    db.session.commit()
    word = Word.query.get(req['wordId'])
    return jsonify({"status": 200, "message": word.en_word})


@api.route('/fix_stat', methods=['POST'])
def fix_stat():
    req = request.json
    row = UserStat.query.filter(UserStat.user_id == req['userId'], UserStat.word_id == req['wordId']).first()
    if row is None:
        new_row = UserStat(user_id=req['userId'], word_id=req['wordId'], correct_attempts=1 if req['result'] else 0,
                           wrong_attempts=1 if not req['result'] else 0, last_try_time=get_current_date())
        db.session.add(new_row)
    else:
        if req['result']:
            row.correct_attempts += 1
        else:
            row.wrong_attempts += 1
        row.last_try_time = get_current_date()
    db.session.commit()
    return jsonify({"status": 200, "message": 'done'})


@api.route('/login', methods=['POST'])
def login_user():
    req = request.json
    user = User.query.filter_by(username=req['username']).first()
    if user is None or not user.check_password(req['password']):
        return jsonify({"status": 400, "message": 'Wrong login or password'})
    else:
        return jsonify({"status": 200, "message": f'{user.id}_{user.first_name}'})


@api.route('/user_stat/<user_id>')
def get_user_stat(user_id):
    stats = db.session.query(Word.en_word, UserStat.correct_attempts, UserStat.wrong_attempts) \
        .join(Word, Word.id == UserStat.word_id) \
        .filter(UserStat.user_id == user_id)\
        .order_by(Word.en_word).all()
    user_stats = []
    for word in stats:
        user_stats.append({'enWord': word[0], 'correctAttempts': word[1], 'wrongAttempts': word[2]})
    return jsonify(user_stats)
