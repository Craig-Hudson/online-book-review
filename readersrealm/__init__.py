import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

if os.path.exists("env.py"):
    import env  # noqa

app = Flask(__name__)

# Database configuration
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")



if os.environ.get("DEVELOPMENT") == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")  # local
else:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri  # heroku

# Additional database configuration options
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

mail_settings = { 
    "MAIL_SERVER": os.environ.get('MAIL_SERVER'), 
    "MAIL_PORT": os.environ.get('MAIL_PORT'), 
    "MAIL_USE_TLS": False, 
    "MAIL_USE_SSL": os.environ.get('MAIL_USE_SSL'), 
    "MAIL_USERNAME": os.environ.get('MAIL_USERNAME'), 
    "MAIL_PASSWORD": os.environ.get('MAIL_PASSWORD'), 
    "SECURITY_EMAIL_SENDER": 
os.environ.get("SECURITY_EMAIL_SENDER") 
}

app.config.update(mail_settings)


# Initialize Flask extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

from readersrealm import routes
