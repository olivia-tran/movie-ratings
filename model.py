"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Replace this with your code!
class User(db.Model):
    """A user"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User ID={self.user_id}, email={self.email}>"

    @classmethod
    def create(cls, email, password):
        """Create and return a new user."""

        return cls(email=email, password=password)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(User.email == email).first()

    @classmethod
    def all_users(cls):
        return cls.query.all()


class Movie(db.Model):

    __tablename__ = "movies"
    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)

    def __repr__(self):
        return f"<MovieId movie_id={self.movie_id} title={self.title} relDate={self.release_date}>"


class Rating(db.Model):
    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # 1st argument is name of the class the attribute will be associated with, 2nd argument is the name of the attribute the 1st class has access to)
    movie = db.relationship('Movie', backref='ratings')
    user = db.relationship('User', backref='ratings')

    def __repr__(self):
        return f"<Ratings: Movie={self.movie_id}, rating_id={self.rating_id}, Score = {self.score} by User={self.user_id}>"

    @classmethod
    def create(cls, user, movie, score):
        """Create and return a new movie"""
        return cls(user=user, movie=movie, score=score)

    @classmethod
    def update(cls, rating_id, new_score):
        """Update a rating given rating_id and the updated score"""
        rating = cls.query.get(rating_id)
        rating.score = new_score


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
