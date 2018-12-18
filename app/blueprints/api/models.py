"""
Physical data models and mixin classes stored in the application's database
"""
from app.models import db

class BaseSerializerMixin(object):
    """
    Provide functionality for serializing db.Models into dicts
    """
    def __init__(self):
        self.__table__ = None

    def serialize(self):
        return {c.name : getattr(self, c.name) for c in self.__table__.columns}


class SerializerMixin(BaseSerializerMixin):
    """
    Extend serialization functionality for db.Models with child models
    """
    def serialize(self):
        serializedSelf = super().serialize()
        for relation in self.__mapper__.relationships.keys():
            serializedSelf[relation] = [o.serialize() for o in getattr(self, relation)]
        return serializedSelf


class User(db.Model, BaseSerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25), unique=True, nullable=False)


class Workout(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    body_weight = db.Column(db.Float, unique=False, nullable=True)
    start_time = db.Column(db.Integer, unique=False, nullable=False)
    end_time = db.Column(db.Integer, unique=False, nullable=False)
    rating_pre = db.Column(db.Integer, unique=False, nullable=True)
    rating_post = db.Column(db.Integer, unique=False, nullable=True)
    exercises = db.relationship('Exercise', backref='workout', lazy=True)


class Exercise(db.Model, BaseSerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    index = db.Column(db.Integer, unique=False, nullable=False)