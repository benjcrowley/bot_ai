"""CRUD operations"""

from model import db, User, Script, Reviews, connect_to_db

# create all user functions
def create_user(username, email, password):
    """Create and return a new user"""

    user = User(username=username, email=email, password=password)

    return user


# view all users
def view_all_users():
    """View all users in the database"""

    users = User.query.all()

    return users


# get user by email or username
def get_user(email_username):
    """Get user by email or username"""

    user = User.query.filter(
        (User.email == email_username) | (User.username == email_username)
    ).first()

    return user


def get_user_by_id(user_id):
    """Get user by id"""

    user = User.query.filter(User.id == user_id).first()

    return user


# create script functions
def create_script(title, description, price, image_file, file_name):
    """Create and return a new script"""

    script = Script(
        title=title,
        description=description,
        price=price,
        image_file=image_file,
        file_name=file_name,
    )

    return script


# view all scripts
def view_all_scripts():
    """View all scripts in the database"""

    return Script.query.all()


# create a review function
def create_review(rating, review, user, script):
    """Create and return a new review"""

    review = Reviews(rating=rating, review=review, user=user, script=script)

    return review


# view all reviews
def view_all_reviews():
    """View all reviews in the database"""

    reviews = Reviews.query.all()

    return reviews


# get all reviews by user id
def get_user_reviews(user_id):
    """Get all reviews by user id"""

    reviews = Reviews.query.filter(Reviews.user_id == user_id).all()

    return reviews


def get_script_by_id(script_id):
    """Get a script by id"""

    script = Script.query.filter(Script.id == script_id).first()

    return script


def get_script_rating(script_id):
    """Get the average rating for a script"""

    script = Script.query.filter(Script.id == script_id).first()
    average_rating = 0
    for review in script.reviews:
        average_rating += review.rating
    # return the average to 1 decimal place
    return round(average_rating / len(script.reviews), 1)


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    print("Connected to DB.")
