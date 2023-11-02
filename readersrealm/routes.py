from flask import(
    render_template,
    request, 
    redirect, 
    url_for,
    flash,
    session)
from readersrealm import app, db
from readersrealm.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Password pattern that enforces at least 8 characters with 1 number and 1 special character
password_pattern = r'^(?=.*[0-9])(?=.*[!@#$%^&*()_+|~=\-\\[\];\',./{}:<>?])([A-Za-z0-9!@#$%^&*()_+|~=\-\\[\];\',./{}:<>?]){8,}$'

def is_valid_password(password):
    return re.match(password_pattern, password) is not None

@app.route("/")
def index():
    return render_template("index.html")

# Define a route for the registration page
@app.route('/register')
def register():
    return render_template('register.html')

# Define a route for processing the registration form
@app.route('/register_post', methods=['GET', 'POST'])
def register_post():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')
        print("Form Data:", request.form)

        if not is_valid_password(password):
            flash("Password must be at least 8 characters long and contain 1 number and 1 special character.", 'error')
            return render_template('register.html')

        # Check if the username and email are already in use
        user = User.query.filter_by(username=username).first()
        email_user = User.query.filter_by(email=email).first()

        if user or email_user:
            flash('Username or email already in use.', 'error')
            return render_template('register.html')

        if password != password_confirmation:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        # Hash the password before storing it in the database
        password_hash = generate_password_hash(password)

        # Create a new user record
        new_user = User(username=username, email=email, password=password_hash,
                         password_confirmation=password_hash)  # Store the hashed password

        # Add the new user record to the database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful!', 'success')
        return redirect('/login')

    return render_template('register.html', username=username, email=email)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Successful login
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to the home page or another protected page
        else:
            # Invalid login
            flash('Invalid username or password. Please try again.', 'error')

    return render_template("login.html")

