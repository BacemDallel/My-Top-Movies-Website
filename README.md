This Flask-based web application serves as a movie review platform. Users can add, rate, review, and delete movies in the database, view a list of movies, and update movie ratings and reviews. The application utilizes The Movie Database (TMDB) API to fetch movie details, such as title, release year, overview, poster image, etc.

Key Features:

Add Movie: Users can search for movies using the TMDB API, select from the search results, and add them to the local database. The app fetches movie details (title, year, description, poster) from the API and assigns a ranking to the added movie.

View Movie List: Displays a list of movies present in the database. The movies are sorted by their ranking.

Rate and Review: Users can rate movies out of 10 and add their reviews. They have the option to edit the movie details by updating its rating and review.

Delete Movie: Allows users to remove a movie from the database. Upon deletion, the movie ranking gets adjusted for the remaining movies.

Technologies Used:

Flask: A Python-based web framework used for backend development.

SQLAlchemy: An ORM (Object-Relational Mapping) library to manage the SQLite database.

Flask-WTF: Handles web forms and input validation.

Flask-Bootstrap: Utilized for front-end development to enhance the UI.

Requests: Used to make HTTP requests to interact with the TMDB API.

The Movie Database (TMDB) API: External API for fetching movie details like title, description, release year, and poster images.

Usage:

The application can be accessed via a web browser. Users can search and add movies, view and interact with the existing movie list, rate and review movies, and delete movies from the database.This Flask-based web application serves as a movie review platform. Users can add, rate, review, and delete movies in the database, view a list of movies, and update movie ratings and reviews. The application utilizes The Movie Database (TMDB) API to fetch movie details, such as title, release year, overview, poster image, etc.

Key Features:

Add Movie: Users can search for movies using the TMDB API, select from the search results, and add them to the local database. The app fetches movie details (title, year, description, poster) from the API and assigns a ranking to the added movie.

View Movie List: Displays a list of movies present in the database. The movies are sorted by their ranking.

Rate and Review: Users can rate movies out of 10 and add their reviews. They have the option to edit the movie details by updating its rating and review.

Delete Movie: Allows users to remove a movie from the database. Upon deletion, the movie ranking gets adjusted for the remaining movies.

Technologies Used:

Flask: A Python-based web framework used for backend development.

SQLAlchemy: An ORM (Object-Relational Mapping) library to manage the SQLite database.

Flask-WTF: Handles web forms and input validation.

Flask-Bootstrap: Utilized for front-end development to enhance the UI.

Requests: Used to make HTTP requests to interact with the TMDB API.

The Movie Database (TMDB) API: External API for fetching movie details like title, description, release year, and poster images.

Usage:

The application can be accessed via a web browser. Users can search and add movies, view and interact with the existing movie list, rate and review movies, and delete movies from the database.
