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
    """
    Function to render the index html page, and to display on the home page
    the two books with the highest ratings.
    """
    active_page = 'index'
    featured_books = Book.query.join(Review).group_by(Book.id).order_by(db.func.sum(Review.rating).desc()).limit(2).all()

    return render_template("index.html", active_page=active_page, featured_books=featured_books)


@app.route('/register')
def register():
    """
    Function to render the register html page 
    """
    active_page = 'register'
    return render_template('register.html', active_page=active_page)


@app.route('/register_post', methods=['GET', 'POST'])
def register_post():
    """ 
    Function for users to register to the website
    get the input from the form,
    then check to see if the password is valid using the is valid password function,
    and display message to inform user,then check if the password and password confirmation match,
    then check if the username or email is already in use, if so flash message to inform user.
    Then create a variable that will store a hashed password to go into the database,
    then send users details to be stored in the database
    """
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')

        if not is_valid_password(password):
            flash("Password must be at least 8 characters long and contain 1 number and 1 special character.", 'error')
            return render_template('register.html')
        
        # Error handling to check weather the password and password confirmation match.
        if password != password_confirmation:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        # Check if the username and email are already in use
        user = User.query.filter_by(username=username).first()
        email_user = User.query.filter_by(email=email).first()

        # Error handling to check weather username or email has already been taken
        if user or email_user:
            flash('Username or email already in use.', 'error')
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
    active_page = 'login'
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

    return render_template("login.html", active_page=active_page)


@app.route('/logout')
def logout():
    """ 
    Function to clear all session data to log out the user,
    and redirect them to home page
    """
    session.clear()  # Clear all session data
    return redirect(url_for('index'))


@app.route('/browse_books')
def browse_books():
    """ 
    Function that will display all the books that users have entered into the database.
    """
    active_page = 'browse_books'
    books = Book.query.all()
    return render_template('browse-books.html', books=books, active_page=active_page)
   

@app.route('/add_book')
def add_book():
    """ 
    Function that will first store the users ID in a variable, and then check if 
    the user is logged in, if not redirect user to login page, 
    if user is logged in render the template for user to access
    """
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
    """ 
    Function to allow users to edit books they've added
    first check if user is logged in, then check if book still exists,
    then check if the user id of the current user matches the user id in the book table,
    and if it does commit changes to the database.
    """
    # Checks if user is in session, if not redirect to login page.
    user_id = session.get('user_id')
    if not user_id:
        return redirect('login')
    
    book = Book.query.get(book_id)
    if book is None:
        return not_found_error(404)

    if user_id != book.user_id:
        return forbidden_error(403)

    if request.method == 'POST':
        # Handle the form submission with the updated book data
        book.title = request.form.get('title')
        book.author_name = request.form.get('author_name')
        book.description = request.form.get('description')
        book.publication_year = request.form.get('publication_year')
        book.genre = request.form.get('genre')
        book.url = request.form.get('image_url')
        if not request.form.get('image_url'):
            book.image_url = "/static/images/not-available.webp"
        else:
            book.image_url = request.form.get('image_url')

        # Check if user id matches user id in the books table
        if user_id == book.user_id:
            db.session.commit()
            
        flash('Your book has successfully been updated', 'success')  
        return redirect(url_for('edit_book', book_id=book_id))


    return render_template('edit-book.html', book=book)


@app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    """ 
    Function to delete books.
    Check if book exists and then check if user in session matches the 
    user id in the book table then delete book from database
    """
    # Retrieve the book from the database
    book = Book.query.get(book_id)
    if book is None:
            return not_found_error(404)

    if book:
        # Check if the logged-in user is the owner of the book
        if 'user_id' in session and session['user_id'] == book.user_id:
            # Delete the book from the database
            db.session.delete(book)
            db.session.commit()
        else:
            return forbidden_error(403)

    # Redirect back to the profile
    return redirect(url_for('profile', username=session.get('username')))



@app.route('/reviews/<book_id>', methods=["GET", "POST"])
def reviews(book_id):
    """ 
    function to display reviews matched with the book's ID
    check if the book exists first, if not 404, 
    then query the database for reviews on that given book, and display on the reviews page.
    """
    try:
        book = Book.query.get(book_id)
        if book is None:
            return not_found_error(404)
        
        reviews = Review.query.filter_by(book_id=book.id).all()

        return render_template('reviews.html', book=book, reviews=reviews)

    except Exception as e:
        return internal_server_error(e)


@app.route('/add_review/<book_id>', methods=['GET', 'POST'])
def add_review(book_id):
    """
    Function for users to add reviews.
    First check if users are logged in to add a review, then check if the book exists.
    Then get the form data including getting the users ID and then add and commit to the database
    """
    try:
        # Check if the user is logged in
        user_id = session.get('user_id')

        if 'user_id' not in session:
            session['login_required'] = True 
            flash('Please log in to add a review.', 'error')
            return redirect(url_for('login'))

        book = Book.query.get(book_id) 
        if book is None:
            return not_found_error(404)

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

    except Exception as e:
        return internal_server_error(e)



@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    """ 
    Function to allow users to edit reviews 
    if user isn't logged in, get user to log in
    check if the review and book exists, if not 404.
    if review form is posted check is user id matches the user id 
    in the review table, then commit new details of the review to the database.
    """
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in to edit a review.', 'error')
        return redirect(url_for('login'))

    review = Review.query.get(review_id)
    if review is None:
        return not_found_error(404)
    
    book = Book.query.get(review.book_id)
    if book is None:
       return not_found_error(404)

    if request.method == 'POST':
        # Handle the form submission with the updated review data
        new_rating = request.form.get('rating')
        new_comment = request.form.get('comment')
        
        user_id = session.get('user_id')
        if user_id == review.user_id:

            # Update the review in the database with the new data
            review.rating = new_rating
            review.comment = new_comment
            db.session.commit()
        
            flash('Review updated successfully!', 'success')
            return redirect(url_for('edit_review', review_id=review.id))
        else:
            return forbidden_error(403)
    
    return render_template('edit-review.html', review=review, book=book, review_id=review_id)



@app.route('/delete_review/<int:review_id>')
def delete_review(review_id):
    """
    Function to delete reviews, if no review found send 404 error.
    Then check is the current logged in user id matches the 
    user id of the review, and if not  and if so delete review from database.
    Then direct user back to their profile page.

    """
    review = Review.query.get(review_id)
    if not review:
        return not_found_error(404)

    # Retrieve the current user's ID from the session
    user_id = session.get('user_id')
    if user_id != review.user_id:
        return forbidden_error(403)

    db.session.delete(review)
    db.session.commit()

    flash('Review deleted successfully.', 'success')

    # Redirect to the profile of the user
    return redirect(url_for('profile', username=session.get('username')))


@app.route('/profile/<username>')
def profile(username):
    """
    Render the user profile page.
    If the user is not logged in, they are redirected to the login page with an error message.
    If the requested username matches the session username, the user's profile is displayed.
    If the requested username does not match the session username, an unauthorized access error is flashed.
    If the requested username does not exist, a user not found error is flashed.
    """
    active_page = 'profile'

    # Get session username
    if session.get('username'):
        current_username = session['username']

        # If current user tries accessing profiles, send to 403 Forbidden error
        if not current_username:
            return forbidden_error(403)

        if username == current_username:
            user = User.query.filter_by(username=username).first()

            # If user ID's match review and books ID's display on users profile
            if user:
                review_ids = [review.id for review in Review.query.filter_by(user_id=user.id).all()]
                reviews = Review.query.filter_by(user_id=user.id).all()
                books = Book.query.filter_by(user_id=user.id).all()
                return render_template('profile.html', active_page=active_page, user=user, reviews=reviews, books=books, review_ids=review_ids)
            else:
                return not_found_error(404)
        else:
            return forbidden_error(403)
    else:
        flash('Please log in to view profiles.', 'error')
        return redirect(url_for('login'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Function to render the contact.html page 
    """
    active_page = 'contact'
    return render_template("contact.html", active_page=active_page)



@app.route('/search', methods=['POST'])
def search():
    """
    Function to get the form data in the search bar
    which will then display the results of the search
    on a search page, if no results are found, the users
    will be informed
    """
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
    error_number = 404
    error_message = 'Page Not Found'
    return render_template('error.html', error_number=error_number, error_message=error_message), error_number

@app.errorhandler(500)
def internal_server_error(error_number):
    error_number = 500
    error_message = 'Internal Server Error'

    return render_template('error.html', error_number=error_number, error_message=error_message), error_number


@app.errorhandler(Exception)
def generic_error(error_number):
    error_number = 500
    return render_template('error.html', error_number=error_number, error_message='Something went wrong'), 500


@app.errorhandler(403)
def forbidden_error(error_number):
    error_number = 403
    return render_template('error.html', error_number=error_number, error_message='Forbidden'), 403
