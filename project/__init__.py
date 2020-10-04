from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_login import LoginManager 
from flask_bcrypt import Bcrypt 
from flask_uploads import configure_uploads, IMAGES, UploadSet
from flask_mail import Mail


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')



db = SQLAlchemy(app)

ma = Marshmallow(app)

login_manager = LoginManager(app)

bcrypt = Bcrypt(app)

images = UploadSet('images', IMAGES, default_dest=lambda x: 'images')

configure_uploads(app, images)

mail = Mail(app)

from project.site.routes import mod
from project.api.routes import mod
from project.users.routes import mod
from project.posts.routes import mod 

app.register_blueprint(site.routes.mod)
app.register_blueprint(api.routes.mod, url_prefix='/api')
app.register_blueprint(users.routes.mod, url_prefix='/users')
app.register_blueprint(posts.routes.mod, url_prefix='/posts')