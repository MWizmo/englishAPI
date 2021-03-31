from app import app, db, login_manager
from flask import request, jsonify, send_from_directory, render_template, redirect, url_for, flash
from app.models import *
from app.forms import *
from flask_login import login_required, login_user, logout_user
from app import utils


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/favicon.ico')
def static_from_root_favicon():
    return send_from_directory(app.static_folder, request.path[1:])


# @app.route("/")
# @login_required
# def home():
#     return render_template("home.html")


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


@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is None:
            user = User(username=form.username.data, created_at=utils.get_current_date())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return render_template('home.html')
        else:
            return render_template("register.html", form=form, error_message='This username is busy')
    return render_template("register.html", form=form)


@app.route("/add_module", methods=['GET', 'POST'])
@login_required
def add_module():
    form = AddModuleForm()
    if form.validate_on_submit():
        if Module.query.filter_by(title=form.title.data).first() is None:
            module = Module(title=form.title.data)
            db.session.add(module)
            db.session.commit()
            flash("Added", "success")
            return redirect('/add_module')
        else:
            return render_template("add_module.html", form=form, error_message='This module exists')
    return render_template("add_module.html", form=form)


@app.route("/add_section", methods=['GET', 'POST'])
@login_required
def add_section():
    form = AddSectionForm()
    modules = Module.query.all()
    if form.validate_on_submit():
        if Section.query.filter_by(title=form.title.data).first() is None:
            section = Section(title=form.title.data, module_id=int(form.module.data))
            db.session.add(section)
            db.session.commit()
            flash("Added", "success")
            return redirect('/add_section')
        else:
            return render_template("add_section.html", form=form, error_message='This section exists',
                                   modules=modules)
    return render_template("add_section.html", form=form, modules=modules)


@app.route('/add_word', methods=['GET', 'POST'])
@login_required
def add_word():
    section_id = int(request.args.get('section_id')) if 'section_id' in request.args else -1
    sections = Section.query.all()
    form = AddWordForm()
    if form.validate_on_submit():
        if Word.query.filter_by(en_word=form.en_word.data.capitalize()).first() is None:
            word = Word(en_word=form.en_word.data.capitalize(), ru_word=form.ru_word.data.capitalize(),
                        part_of_speech=form.part_of_speech.data.capitalize(),
                        section_id=int(form.theme.data), definition=form.definition.data.capitalize())
            db.session.add(word)
            db.session.commit()
            flash("Added", "success")
            return redirect(f'/add_word?section_id={form.section.data}')
        else:
            return render_template("add_theme.html", form=form, error_message='This word exists',
                                   current_section=section_id, sections=sections)
    return render_template("add_word.html", form=form, current_section=section_id, sections=sections)


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