from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin


app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

from app import routes, models, views
from app.api_routes import api

app.register_blueprint(api, url_prefix='/api')
admin = Admin(app, name='Academic English', template_mode='bootstrap3', index_view=views.IndexView(url='/'))
admin.add_view(views.ModuleView(models.Module, db.session, name='Modules'))
admin.add_view(views.SectionView(models.Section, db.session, name='Sections'))
admin.add_view(views.WordView(models.Word, db.session, name='Words'))
admin.add_view(views.CollocationView(models.Collocation, db.session, name='Collocations'))
admin.add_view(views.SentenseView(models.Sentense, db.session, name='Sentenses'))
admin.add_view(views.TasksView(models.Module, db.session, name='Tasks', endpoint='tasks'))
admin.add_view(views.UsersView(models.User, db.session, name='Users'))
