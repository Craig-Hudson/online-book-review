from flask import(
    render_template,
    request, 
    redirect, 
    url_for,
    flash,
    session)
from readersrealm import app, db
from readersrealm.models import User, Author, Book
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

        # Error handling to check weather username or email has already been taken
        if user or email_user:
            flash('Username or email already in use.', 'error')
            return render_template('register.html')
        
        # Error handling to check weather the password and password confirmation match.
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
    """
    Function to log users in by getting the information from that database
    also using error handling to ensure the user has entered the correct
    username and password
    """
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Successful login
            session['logged_in'] = True
            session['user_id'] = user.id
            return redirect(url_for('index'))  # Redirect to the home page
        else:
            # Invalid login
            flash('Invalid username or password. Please try again.', 'error')

    return render_template("login.html")



@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('index'))


@app.route('/browse_books')
def browse_books():
    books = Book.query.all()
    return render_template('browse-books.html', books=books)


@app.route('/add_book')
def add_book():
    return render_template('add-book.html')


@app.route('/add_book_form', methods=['GET', 'POST'])
def add_book_form():
    """
    Function to firstly retrieve the form data, then checks if an author is already in the database
    if not then add new author to the database.
    then add all the details associated with the book to the database
    """
    if request.method == 'POST':
        title = request.form['title']
        author_name = request.form['author_name']  # User-provided author name
        description = request.form['description']
        publication_year = request.form['publication_year']
        image_url= request.form['image_url']
        genre = request.form['genre']

        # Check if the author already exists in the database
        author = Author.query.filter_by(name=author_name).first()

        if not author:
            # If the author doesn't exist, create a new author
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()
        
        if not image_url:
            image_url = url_for('static', filename='not-available.webp')

        user_id = session.get('user_id')

        # Check if a book with the same title and author already exists
        existing_book = Book.query.join(Author).filter(
                        Book.title == title, Author.name == author_name).first()

        if existing_book:
            flash('This book already exists.', 'error')
            return redirect(url_for('add_book_form'))

        new_book = Book(title=title,
                        author_id=author.id,
                        description=description,
                        publication_year=publication_year,
                        image_url=image_url,
                        user_id=user_id,
                        genre=genre)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('browse_books')) 

    return render_template('add-book.html')  # Render the book entry form

