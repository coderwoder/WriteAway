from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


db= SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='users.login' #For 'login_required', We need to tell the extension where the login route is.
login_manager.login_message_category = 'info'
mail=Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.user.routes import users
    app.register_blueprint(users)
    from flaskblog.post.routes import posts
    app.register_blueprint(posts)
    from flaskblog.main.routes import main
    app.register_blueprint(main)
    from flaskblog.errors.errors import errors
    app.register_blueprint(errors)

    return app