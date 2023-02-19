from flask import request
from flask_restx import Namespace, Resource

from models import Director, directors_schema, director_schema
from setup_db import db

director_ns = Namespace('directors')

@director_ns.route('/')
class DirectorViews(Resource):
    def get(self):
        all_directors = Director.query.all()
        return directors_schema.dump(all_directors), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "Director created", 201


@director_ns.route('/<did>')
class DirectorView(Resource):
    def get(self, did):
        try:
            director = Director.query.get(did)
            return director_schema.dump(director), 200
        except Exception:
            return str(Exception), 404

    def put(self, did):
        updated_rows = db.session.query(Director).filter(Director.id == did).update(request.json)
        if updated_rows != 1:
            return "Not updated", 400
        db.session.commit()
        return "", 204

    def delete(self, did):
        director = Director.query.get(did)
        if not director:
            return "Movie not found", 404
        db.session.delete(director)
        db.session.commit()
        return "", 204
