"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import model
import server
import crud

os.system("dropdb ratings")

os.system("createdb ratings")
model.connect_to_db(server.app)
model.db.create_all()
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

movies_in_db = []
for movie in movie_data:
    release_date = datetime.strptime(movie['release_date'], '%Y-%m-%d')

    movie_ind_db = crud.create_movie(title=movie['title'], overview=movie['overview'],
                                     release_date=release_date, poster_path=movie['poster_path'])
    movies_in_db.append(movie_ind_db)

model.db.session.add_all(movies_in_db)
model.db.session.commit()
