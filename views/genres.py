from flask import request
from flask_restx import Namespace, Resource

from models import Genre, genres_schema, genre_schema
from setup_db import db

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenreViews(Resource):
    def get(self):
        all_genres = Genre.query.all()
        return genres_schema.dump(all_genres), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "Genre created", 201


@genre_ns.route('/<gid>')
class GenreView(Resource):
    def get(self, gid):
        genre = Genre.query.get(gid)
        return genre_schema.dump(genre), 200

    def put(self, gid):
        updated_rows = db.session.query(Genre).filter(Genre.id == gid).update(request.json)
        if updated_rows != 1:
            return "Not updated", 400
        db.session.commit()
        return "", 204

    def delete(self, gid):
        genre = Genre.query.get(gid)
        if genre is None:
            return "Genre not found", 404
        db.session.delete(genre)
        db.session.commit()
        return "", 204
