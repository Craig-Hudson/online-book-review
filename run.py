import os
from flask import Flask
from readersrealm import app, db
from flask_migrate import Migrate
from flask_mail import Mail, Message



# Initialize Flask-Migrate
migrate = Migrate(app, db)



if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG") == "True"
    )

# mail_settings = { 
#     "MAIL_SERVER": os.environ.get('MAIL_SERVER'), 
#     "MAIL_PORT": os.environ.get('MAIL_PORT'), 
#     "MAIL_USE_TLS": False, 
#     "MAIL_USE_SSL": os.environ.get('MAIL_USE_SSL'), 
#     "MAIL_USERNAME": os.environ.get('MAIL_USERNAME'), 
#     "MAIL_PASSWORD": os.environ.get('MAIL_PASSWORD'), 
#     "SECURITY_EMAIL_SENDER": 
# os.environ.get("SECURITY_EMAIL_SENDER") 
# }

# app.config.update(mail_settings)
# mail = Mail(app)

@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db}
