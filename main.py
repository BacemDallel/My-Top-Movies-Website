from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from sqlalchemy import desc, asc
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

##CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy()
db.init_app(app)

MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie?"
MOVIE_DB_API_KEY = '1e72f334eff54926c31ee61ed34ebd96'
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = 'https://image.tmdb.org/t/p/original/'

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZTcyZjMzNGVmZjU0OTI2YzMxZWU2MWVkMzRlYmQ5NiIsInN1YiI6IjY1NzljNTAwNTY0ZWM3MDExYjIxMDZmNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.6zLOc2MvMUKIKmASObyTfVxS_0c8T2QuSHMMU5UCVnQ"
}


##CREATE TABLE
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)  # Make 'rating' field nullable
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()

class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")



class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")

@app.route("/")
def home():
    all_movies = Movie.query.order_by(asc(Movie.rating)).all()

    return render_template("index.html", movies=all_movies)

# Adding the Update functionality
@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)

@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": movie_title})
        data = response.json().get('results', [])  # Check for 'results' key in response
        return render_template("select.html", data=data)
    return render_template('add.html', form=form)


# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )
# with app.app_context():
#     db.session.add(second_movie)
#     db.session.commit()



@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, headers=headers)
        data = response.json()

        # Get the last movie and its ranking from the database
        last_movie = Movie.query.order_by(Movie.id.desc()).first()
        last_ranking = last_movie.ranking if last_movie else 0

        # Create a new movie with an incremented ranking
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            description=data["overview"],
            rating=0.0,  # Assign a default rating (change as needed)
            ranking=last_ranking + 1,  # Increment the ranking
            review='',
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
        )

        with app.app_context():
            db.session.add(new_movie)
            db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)

    movie_ranking = movie.ranking

    db.session.delete(movie)
    db.session.commit()

    movies_to_update = Movie.query.filter(Movie.ranking > movie_ranking).all()
    for movie in movies_to_update:
        movie.ranking -= 1

    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run()