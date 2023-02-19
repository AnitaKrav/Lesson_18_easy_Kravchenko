# здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки). сюда импортируются сервисы из пакета service
from flask import request
# Пример
from flask_restx import Resource, Namespace

from models import Movie, movies_schema, movie_schema
from setup_db import db

movie_ns = Namespace('movies')

@movie_ns.route('/')
class BooksView(Resource):
    def get(self):
        all_movies = db.session.query(Movie)
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        if director_id is not None:
            all_movies = all_movies.filter(Movie.director_id == director_id)
        if genre_id is not None:
            all_movies = all_movies.filter(Movie.genre_id == genre_id)
        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "Movie created", 201


# ----------MovieViews--------------
@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)
        if not movie:
            return "Movie not found", 404
        return movie_schema.dump(movie), 200

    def put(self, mid):
        updated_rows = db.session.query(Movie).filter(Movie.id == mid).update(request.json)
        if updated_rows != 1:
            return "Not updated", 400
        db.session.commit()
        return "", 204


    def delete(self, mid):
        movie = Movie.query.get(mid)
        if not movie:
            return "Movie not found", 404
        db.session.delete(movie)
        db.session.commit()
        return "", 204

