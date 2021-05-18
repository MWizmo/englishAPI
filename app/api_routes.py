# -*- coding: utf-8 -*-
import os
from flask import jsonify, request, Blueprint, send_from_directory
from app.models import *
import random
import re
from datetime import datetime as dt
from app import app

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
                 'sectionId': word.section.id, 'audio': word.audio}
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
    for row in Dictionary.query.filter_by(user_id=user_id).all():
        word = Word.query.get(row.word_id)
        word_info = {'id': word.id, 'enWord': word.en_word, 'ruWord': word.ru_word, 'section': word.section.title,
                     'definition': word.definition, 'partOfSpeech': word.part_of_speech, 'sectionId': word.section.id}
        words.append(word_info)
    return jsonify(words)


@api.route('/user_collocations/<user_id>')
def get_collocations_of_user(user_id):
    collocations = []
    for row in CollocationDictionary.query.filter_by(user_id=user_id).all():
        coll = Collocation.query.get(row.collocation_id)
        info = {'id': coll.id, 'firstPart': coll.first_part, 'secondPart': coll.second_part,
                             'ruTranslation': coll.ru_translation, 'inDictionary': True}
        collocations.append(info)
    return jsonify(collocations)


@api.route('/words/<section_id>')
def get_words_of_section(section_id):
    words = []
    for word in Word.query.filter_by(section_id=section_id).all():
        words.append(get_word_info(word.id))
    return jsonify(words)


@api.route('/collocations/<section_id>')
def get_collocations_of_section(section_id):
    collocations = []
    for coll in Collocation.query.filter_by(section_id=section_id).all():
        collocations.append({'id': coll.id, 'firstPart': coll.first_part, 'secondPart': coll.second_part,
                            'ruTranslation': coll.ru_translation, 'inDictionary': False})
    return jsonify(collocations)


@api.route('/collocation/<coll_id>&<user_id>')
def get_collocation_by_id(coll_id, user_id):
    coll = Collocation.query.get(coll_id)
    query = CollocationDictionary.query.filter(CollocationDictionary.collocation_id == coll_id,
                                                    CollocationDictionary.user_id == user_id).first()
    inDictionary = query is not None
    info = {'id': coll.id, 'firstPart': coll.first_part, 'secondPart': coll.second_part,
                            'ruTranslation': coll.ru_translation, 'inDictionary': inDictionary, 'audio': coll.audio}
    return jsonify(info)


@api.route('/word/<word_id>&<user_id>')
def get_word_by_id(word_id, user_id):
    return jsonify(get_word_info(word_id, user_id))


@api.route('/tasks/<section_id>&<user_id>')
def get_tasks_of_section(section_id, user_id):
    tasks = TaskInSection.query.filter_by(section_id=section_id).all()
    tasks_info = []
    for t in tasks:
        completed = UserTask.query.filter(UserTask.user_id==user_id, UserTask.task_id==t.id).first() is not None
        tasks_info.append({'type': t.task_type, 'taskId': t.task_id, 'id': t.id, 'sectionId': t.section_id,
                           'completed': completed})
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
        task.append({'enWord': words[i].en_word, 'ruWord': words[i].ru_word, 'definition': words[i].definition,
                     'isRight': i == rand_index, 'wordId': words[i].id})
    return jsonify(task)


@api.route('/audio_task/<section_id>&<previous_word_id>')
def audio_task(section_id, previous_word_id):
    audio_words = Word.query.filter(Word.section_id == section_id, Word.audio == True).all()
    random.shuffle(audio_words)
    rand_index = random.randint(0, len(audio_words) - 1)
    while audio_words[rand_index].id == previous_word_id:
        random.shuffle(audio_words)
        rand_index = random.randint(0, len(audio_words) - 1)
    word = audio_words[rand_index]
    task = [{'enWord': word.en_word, 'ruWord': word.ru_word, 'isRight': True, 'wordId': word.id, 'definition': ''}]
    words = Word.query.filter(Word.section_id == section_id, Word.id != audio_words[rand_index].id).all()
    random.shuffle(words)
    for i in range(3):
        task.append({'enWord': words[i].en_word, 'ruWord': words[i].ru_word, 'isRight': False,
                     'wordId': words[i].id, 'definition': ''})
    random.shuffle(task)
    return jsonify(task)


@api.route('/make_word_task/<section_id>&<previous_word_id>')
def make_word_task(section_id, previous_word_id):
    words = Word.query.filter_by(section_id=section_id).all()
    random.shuffle(words)
    word = words[0]
    if word.id == previous_word_id:
        word = words[1]
    word_list = list(word.en_word)
    random.shuffle(word_list)
    task = {'enWord': ''.join(word_list), 'ruWord': word.ru_word, 'definition': word.definition,
                     'isRight': True, 'wordId': word.id}
    return jsonify(task)


@api.route('/translation_collocation_task/<section_id>&<previous_coll_id>')
def get_collocations_from_section(section_id, previous_coll_id):
    collocations = Collocation.query.filter_by(section_id=section_id).all()
    random.shuffle(collocations)
    rand_index = random.randint(0, 3)
    while collocations[rand_index].id == previous_coll_id:
        random.shuffle(collocations)
        rand_index = random.randint(0, 3)
    task = []
    for i in range(4):
        task.append({'enWord': collocations[i].full, 'ruWord': collocations[i].ru_translation, 'definition': '',
                     'isRight': i == rand_index, 'wordId': collocations[i].id})
    return jsonify(task)


@api.route('/dictionary_word_task/<user_id>&<previous_word_id>')
def dictionary_word_task(user_id, previous_word_id):
    dict_rows = [d.word_id for d in Dictionary.query.filter_by(user_id=user_id).all()]
    words = [Word.query.get(word_id) for word_id in dict_rows]
    random.shuffle(words)
    rand_index = random.randint(0, 3)
    while words[rand_index].id == previous_word_id:
        random.shuffle(words)
        rand_index = random.randint(0, 3)
    task = []
    for i in range(4):
        task.append({'enWord': words[i].en_word, 'ruWord': words[i].ru_word, 'definition': words[i].definition,
                     'isRight': i == rand_index, 'wordId': words[i].id})
    return jsonify(task)


@api.route('/dictionary_collocation_task/<user_id>&<previous_coll_id>')
def dictionary_collocation_task(user_id, previous_coll_id):
    dict_rows = [d.collocation_id for d in CollocationDictionary.query.filter_by(user_id=user_id).all()]
    collocations = [Collocation.query.get(coll_id) for coll_id in dict_rows]
    random.shuffle(collocations)
    rand_index = random.randint(0, 3)
    while collocations[rand_index].id == previous_coll_id:
        random.shuffle(collocations)
        rand_index = random.randint(0, 3)
    task = []
    for i in range(4):
        task.append({'enWord': collocations[i].full, 'ruWord': collocations[i].ru_translation, 'definition': '',
                     'isRight': i == rand_index, 'wordId': collocations[i].id})
    return jsonify(task)


@api.route('/matching_collocation_task/<section_id>&<previous_coll_id>')
def get_matching_collocations_from_section(section_id, previous_coll_id):
    collocations = Collocation.query.filter_by(section_id=section_id).all()
    random.shuffle(collocations)
    rand_index = random.randint(0, 3)
    while collocations[rand_index].id == previous_coll_id:
        random.shuffle(collocations)
        rand_index = random.randint(0, 3)
    task = []
    for i in range(4):
        task.append({'enWord': collocations[i].first_part, 'ruWord': collocations[i].second_part, 'definition': '',
                     'isRight': i == rand_index, 'wordId': collocations[i].id})
    return jsonify(task)


@api.route('/add_to_dictionary', methods=['POST'])
def add_to_dictionary():
    req = request.json
    if req['isWord']:
        new_row = Dictionary(user_id=req['userId'], word_id=req['wordId'])
        answer = Word.query.get(req['wordId']).en_word
    else:
        new_row = CollocationDictionary(user_id=req['userId'], collocation_id=req['wordId'])
        answer = Collocation.query.get(req['wordId']).full
    db.session.add(new_row)
    db.session.commit()
    return jsonify({"status": 200, "message": answer})


@api.route('/remove_from_dictionary', methods=['POST'])
def remove_from_dictionary():
    req = request.json
    if req['isWord']:
        Dictionary.query.filter(Dictionary.user_id == req['userId'], Dictionary.word_id == req['wordId']).delete()
        answer = Word.query.get(req['wordId']).en_word
    else:
        CollocationDictionary.query.filter(CollocationDictionary.user_id == req['userId'],
                                           CollocationDictionary.collocation_id == req['wordId']).delete()
        answer = Collocation.query.get(req['wordId']).full
    db.session.commit()
    return jsonify({"status": 200, "message": answer})


@api.route('/fix_stat', methods=['POST'])
def fix_stat():
    req = request.json
    if req['wordId'] > 0:
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
    if req['result']:
        row = UserTask.query.filter(UserTask.user_id == req['userId'], UserTask.task_id == req['taskId']).first()
        if not row:
            ut = UserTask(user_id=req['userId'], task_id=req['taskId'])
            db.session.add(ut)
    db.session.commit()
    return jsonify({"status": 200, "message": 'done'})


@api.route('/fix_collocation_stat', methods=['POST'])
def fix_collocation_stat():
    req = request.json
    row = UserCollocationStat.query.filter(UserCollocationStat.user_id == req['userId'],
                                           UserCollocationStat.collocation_id == req['wordId']).first()
    if row is None:
        new_row = UserCollocationStat(user_id=req['userId'], collocation_id=req['wordId'],
                                      correct_attempts=1 if req['result'] else 0,
                                      wrong_attempts=1 if not req['result'] else 0, last_try_time=get_current_date())
        db.session.add(new_row)
    else:
        if req['result']:
            row.correct_attempts += 1
        else:
            row.wrong_attempts += 1
        row.last_try_time = get_current_date()
    if req['result']:
        row = UserTask.query.filter(UserTask.user_id == req['userId'], UserTask.task_id == req['taskId']).first()
        if not row:
            ut = UserTask(user_id=req['userId'], task_id=req['taskId'])
            db.session.add(ut)
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
    stats = db.session.query(Collocation.first_part, Collocation.second_part, UserCollocationStat.correct_attempts, UserCollocationStat.wrong_attempts) \
        .join(Collocation, Collocation.id == UserCollocationStat.collocation_id) \
        .filter(UserCollocationStat.user_id == user_id) \
        .order_by(Collocation.first_part).all()
    for word in stats:
        user_stats.append({'enWord': f'{word[0]} {word[1]}', 'correctAttempts': word[2], 'wrongAttempts': word[3]})
    return jsonify(user_stats)


@api.route('/sentense_task/<section_id>&<previous_sentense_id>')
def sentense_task(section_id, previous_sentense_id):
    sentenses = Sentense.query.filter_by(section_id=section_id).all()
    random.shuffle(sentenses)
    rand_index = random.randint(0, len(sentenses) - 1)
    while sentenses[rand_index].id == previous_sentense_id:
        random.shuffle(sentenses)
        rand_index = random.randint(0, len(sentenses) - 1)
    sentence_id = sentenses[rand_index].id
    sentence = sentenses[rand_index].text
    word_count = sentence.count('{')
    missing_words = []
    for i in range(word_count):
        s = re.search('{\w+}', sentence)
        word = sentence[s.start(): s.end()]
        sentence = sentence.replace(word, '___')
        missing_words.append(word[1:-1])
    task = {'sentence': sentence, 'sentenceId': sentence_id,'blanks': word_count,'words': []}
    all_words = list(Word.query.filter_by(section_id=section_id).all())
    for i, word in enumerate(missing_words):
        w = Word.query.filter_by(en_word=word).first()
        all_words.remove(w)
        task['words'].append({'word': word, 'wordId': w.id, 'order': i + 1})
    random.shuffle(all_words)
    for i in range(len(task['words']), 4):
        w = all_words[i]
        task['words'].append({'word': w.en_word, 'wordId': w.id, 'order': -1})
    random.shuffle(task['words'])
    return jsonify(task)


@api.route('/audio_file/words/<filename>')
def download_audio_word(filename):
        path = app.root_path + '/audio/words'
        report_path = path
        filename = filename + '.mp3'
        report_file = os.path.join(path, filename)
        if os.path.isfile(report_file):
            return send_from_directory(report_path, filename=filename, as_attachment=True)


@api.route('/audio_file/collocations/<filename>')
def download_audio(filename):
        path = app.root_path + '/audio/collocations'
        report_path = path
        filename = filename + '.mp3'
        report_file = os.path.join(path, filename)
        if os.path.isfile(report_file):
            return send_from_directory(report_path, filename=filename, as_attachment=True)

