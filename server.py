"""Server for movie ratings app."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, flash, request, session
from model import connect_to_db, db
import crud


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined




@app.route('/')
def index():
    return render_template('homepage.html')


@app.route("/users")
def all_users():
    users = crud.get_users()
    return render_template("all_users.html", users=users)


@app.route("/users", methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")

    if crud.get_user_by_email(email) == None:
        newUser = crud.create_user(email, password)
        print('this is the if blockn\n')

        flash('Account was succesfully created')
    else:
        # crud.get_user_by_email(email)
        print('this if the else block\n')
        flash('Email already exists.')

    return redirect('/')


@app.route('/users/<user_id>')
def user_details(user_id):
    user_details = crud.get_user_by_id(user_id)
    return render_template("user_details.html", users=user_details)
# <a href="/movies">


@app.route('/login', methods=['POST'])
def to_login():
    flash('Logged In')
    return redirect('/')


@app.route('/movies')
def all_movies():
    '''View all movies'''
    movies = crud.get_movies()
    return render_template("all_movies.html", movies=movies)


@app.route('/movies/<movie_id>')
def movie_details(movie_id):
    movie_details = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie_details)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(debug=True)
