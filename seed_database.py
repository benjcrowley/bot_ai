"""Script to seed database with dummy data"""
import bcrypt
import os
import json
from random import choice, randint
from datetime import datetime

import model
import server

os.system("dropdb scripts")
os.system("createdb scripts")

model.connect_to_db(server.app)
model.db.create_all()

# use with open to open the scripts.json file in the data folder
with open("data/scripts.json") as f:
    script_data = json.loads(f.read())

# loop over each script in the script_data and create a new script object
scripts_in_db = []
for script in script_data:

    title = script["title"]
    description = script["description"]
    price = script["price"]
    image_file = script["image_file"]
    file_name = script["file_name"]

    db_script = model.Script(
        title=title,
        description=description,
        price=price,
        image_file=image_file,
        file_name=file_name,
    )
    scripts_in_db.append(db_script)

model.db.session.add_all(scripts_in_db)
model.db.session.commit()

# create 10 users
users_in_db = []
for n in range(10):
    username = f"user{n}"
    email = f"user{n}@testmail.com"
    password = "test"

    user = model.User(username=username, email=email, password=password)
    users_in_db.append(user)
    # create 5 reviews for each user
    reviews = []
    for i in range(5):
        rating = randint(3, 5)
        review = f"This is review {i} for user {n}"
        script = choice(scripts_in_db)
        review = model.Reviews(rating=rating, review=review, user=user, script=script)
        reviews.append(review)
    model.db.session.add_all(reviews)
model.db.session.add_all(users_in_db)
model.db.session.commit()
