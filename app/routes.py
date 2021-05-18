from app import app, db, login_manager
from flask import request, jsonify, send_from_directory, render_template, redirect, url_for, flash
from app.models import *
from app.forms import *
from flask_login import login_required, login_user, logout_user


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/favicon.ico')
def static_from_root_favicon():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template("login.html", form=form, error_message="Wrong login or password")
        else:
            login_user(user, remember=True)
            redirect_url = request.args.get("next") or url_for("home")
            return redirect(redirect_url)
    return render_template("login.html", form=form)


@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    form = request.form
    s_id = int(form.get('s_id'))
    t_id = int(form.get('t_id'))
    task = TaskInSection(section_id=s_id, task_type=t_id, task_id=0)
    db.session.add(task)
    db.session.commit()
    return jsonify({'status': 'ok'})


@app.route('/delete_task/<task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    TaskInSection.query.filter_by(id=task_id).delete()
    db.session.commit()
    return jsonify({'status': 'ok'})


@app.route('/sentense/new/')
@login_required
def new_sentense():
    sections = Section.query.all()
    return render_template('new_sentense.html', sections=sections)


@app.route('/add_sentense', methods=['POST'])
def add_sentense():
    s_id = int(request.form.get('s_id'))
    texts = request.form.getlist('texts[]')
    blanks = request.form.getlist('blanks[]')
    text = ''
    for i in range(min(len(texts), len(blanks))):
        text += texts[i]
        word = Word.query.get(int(blanks[i]))
        text += ' {' + word.en_word + '} '
    if len(texts) > len(blanks):
        for i in range(min(len(texts), len(blanks)), len(texts)):
            text += texts[i]
    else:
        for i in range(min(len(texts), len(blanks)), len(blanks)):
            word = Word.query.get(int(blanks[i]))
            text += ' {' + word.en_word + '} '
    sentense = Sentense(section_id=s_id, text=text)
    db.session.add(sentense)
    db.session.commit()
    if request.form.get('btn') == 'Save':
        return jsonify({'status': 1, 'url': '/sentense/'})
    else:
        return jsonify({'status': 1, 'url': '/sentense/new/'})


# @app.route('/word/new/')
# def new_word():
#     sections = Section.query.all()
#     return render_template('new_word.html', edit=False, sections=sections)
#
#
# @app.route('/word/edit/')
# def edit_word():
#     word_id = int(request.args.get('id'))
#     sections = Section.query.all()
#     word = Word.query.get(word_id)
#     return render_template('new_word.html', edit=True, sections=sections, word=word)
