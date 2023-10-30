from flask import render_template, request, redirect, url_for, flash
from readersrealm import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from readersrealm.models import User


@app.route("/")
def index():
    return render_template("index.html")

# Define a route for the registration page
@app.route('/register')
def register():
    return render_template('register.html')

# Define a route for processing the registration form
@app.route('/register', methods=['GET', 'POST'])
def register_post():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')

        # Check if the username and email are already in use
        user = User.query.filter_by(username=username).first()
        email_user = User.query.filter_by(email=email).first()

        if user or email_user:
            flash('Username or email already in use.', 'error')
        elif password != password_confirmation:
            flash('Passwords do not match.', 'error')
        else:
            # Hash and salt the password before storing it in the database
            hashed_password = generate_password_hash(password, method='sha256')

            # Create a new user record
            new_user = User(username=username, email=email, password=hashed_password)

            # Add the new user record to the database
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login')
def login():
    render_template('login.html')