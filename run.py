import os
from readersrealm import app, db  # I'm assuming `db` is also defined in `readersrealm`
from flask_migrate import Migrate

# Initialize Flask-Migrate
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG") == "True"
    )

@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db}
