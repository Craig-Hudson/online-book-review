from flask import(
    render_template,
    request, 
    redirect, 
    url_for,
    flash,
    session)
from readersrealm import app, db
from readersrealm.models import User, Author, Book, Review, Genre
from werkzeug.security import generate_password_hash, check_password_hash
import re, os

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
                        password_confirmation=password_hash)

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
            session['username'] = username
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
    # Check if a user is logged in
    user_id = session.get('user_id')

    if user_id is None:
        # User is not logged in, redirect to the login page
        return redirect(url_for('login'))

    # User is logged in, render the 'add-book.html' template
    return render_template('add-book.html')


@app.route('/add_book_form', methods=['GET', 'POST'])
def add_book_form():
    """
    Function to firstly retrieve the form data, then checks if an author is already in the database
    if not then add new author to the database.
    then add all the details associated with the book to the database
    """
    if request.method == 'POST':
        title = request.form.get('title')
        author_name = request.form.get('author_name')  # User-provided author name
        description = request.form.get('description')
        publication_year = request.form.get('publication_year')
        image_url= request.form.get('image_url')
        genre = request.form.get('genre')

        # Check if the author already exists in the database
        author = Author.query.filter_by(name=author_name).first()

        if not author:
            # If the author doesn't exist, create a new author
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()
        
        if not image_url:
            image_url = url_for('static', filename='images/not-available.webp')

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


@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    # Checks if user is in session, if not redirect to login page.
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to edit a book', 'error')
        return redirect('login')
    
    book = Book.query.get(book_id)

    if book_id is None:
        return redirect(url_for('404'))

    if request.method == 'POST':
        # Handle the form submission with the updated book data
        book.title = request.form.get('title')
        book.author_name = request.form.get('author_name')
        book.description = request.form.get('description')
        book.publication_year = request.form.get('publication_year')
        book.genre = request.form.get('genre')
        book.image_url = request.form.get('image_url')

        db.session.commit()

        flash('Book updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit-book.html', book=book)


@app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    # Retrieve the book from the database
    book = Book.query.get(book_id)
    if book is None:
            flash('Book not found.', 'error')
            return render_template('404.html', error='Book not found'), 404

    if book:
        # Check if the logged-in user is the owner of the book
        if 'user_id' in session and session['user_id'] == book.user_id:
            # Delete the book from the database
            db.session.delete(book)
            db.session.commit()
            flash('Book deleted successfully!', 'success')
        else:
            flash('You are not authorized to delete this book.', 'error')

    # Redirect back to the profile
    return redirect(url_for('profile', username=session.get('username')))



@app.route('/reviews/<book_id>', methods=["GET", "POST"])
def reviews(book_id):
    
    book = Book.query.get(book_id)
    if book is None:
        flash('Book not found.', 'error')
        return render_template('404.html', error='Book not found'), 404
    
    reviews = Review.query.filter_by(book_id=book.id).all()

    return render_template('reviews.html', book=book, reviews=reviews)


from flask import redirect, url_for, render_template

@app.route('/add_review/<book_id>', methods=['GET', 'POST'])
def add_review(book_id):
    # Check if the user is logged in
    user_id = session.get('user_id')

    if 'user_id' not in session:
        session['login_required'] = True  # Set the login_required flag
        flash('Please log in to add a review.', 'error')
        return redirect(url_for('login'))

    book = Book.query.get(book_id) 
    if book is None:
        flash('Book not found.', 'error')
        return render_template('404.html', error='Book not found'), 404

    if request.method == 'POST':
        user_id = session['user_id']  # Get the user's ID from the session
        rating = request.form['rating']  # Capture the rating from the form
        comment = request.form['comment']  # Capture the review content (comment)

        # Create a new review with the above data
        new_review = Review(user_id=user_id, book_id=book_id, rating=rating, comment=comment)
        db.session.add(new_review)
        db.session.commit()

        flash('Review added successfully!', 'success')

        # Redirect to the reviews page after adding the review
        return redirect(url_for('reviews', book_id=book_id))

    return render_template('add-review.html', book_id=book_id, book=book)






@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in to edit a review.', 'error')
        return redirect(url_for('login'))

    review = Review.query.get(review_id)
    if review is None:
        flash('Review not found.', 'error')
        return render_template('404.html', error='Review not found'), 404
    
    book = Book.query.get(review.book_id)
    if book is None:
        flash('Book not found.', 'error')
        return render_template('404.html', error='Book not found'), 404

    if request.method == 'POST':
        # Handle the form submission with the updated review data
        new_rating = request.form.get('rating')
        new_comment = request.form.get('comment')
        
        # Update the review in the database with the new data
        review.rating = new_rating
        review.comment = new_comment
        db.session.commit()
        
        flash('Review updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit-review.html', review=review, book=book, review_id=review_id)



@app.route('/delete_review/<int:review_id>')
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return not_found_error(404)
    
    user = None  # Initialize user to None

    if review:
        db.session.delete(review)
        db.session.commit()

      
        user = User.query.get(review.user_id)

    if user:
        # Render the template with the user variable
        return render_template('profile.html', user=user, review_deleted=True)
    else:
        flash('User not found.', 'error')

    # Review not found or user not found
    flash('Review not found or user not found.', 'error')
    return redirect(url_for('profile'))  # Redirect to the profile without a specific username


@app.route('/profile/<username>')
def profile(username):
    if session.get('username'):
        current_username = session['username']
        if not current_username:
            return render_template('404.html')
        if username == current_username:
            user = User.query.filter_by(username=username).first()
            if user:
                review_ids = [review.id for review in Review.query.filter_by(user_id=user.id).all()]
                reviews = Review.query.filter_by(user_id=user.id).all()
                books = Book.query.filter_by(user_id=user.id).all()
                return render_template('profile.html', user=user, reviews=reviews, books=books, review_ids=review_ids)
            else:
                flash('User not found.', 'error')
                return redirect(url_for('index'))
        else:
            flash('Unauthorized access.', 'error')
            return redirect(url_for('index'))
    else:
        flash('Please log in to view profiles.', 'error')
        return redirect(url_for('login'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")



@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search')

    # Perform the search in the database.
    if search_query:
        try:
            search_results = Book.query.join(Author).filter(
                (Book.title.ilike(f"%{search_query}%")) |
                (Book.description.ilike(f"%{search_query}%")) |
                (Author.name.ilike(f"%{search_query}%")) |
                (Book.publication_year == int(search_query))
            ).all()
        except ValueError:
            # Handle the case where search_query is not a valid integer
            search_results = Book.query.join(Author).filter(
                (Book.title.ilike(f"%{search_query}%")) |
                (Book.description.ilike(f"%{search_query}%")) |
                (Author.name.ilike(f"%{search_query}%"))
            ).all()
    else:
        # Displays results as none if an empty string
        search_results = []

    return render_template('search.html', search_results=search_results)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404