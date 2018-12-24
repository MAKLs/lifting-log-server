"""
RESTful API for interacting with application's database of physical data
"""
import functools
from flask import Blueprint, jsonify, request, abort
from app.models import db
from .models import Workout, Exercise

api = Blueprint('api', __name__)

def execute_or_abort(code=404):
    def api_decorator(api_func):
        @functools.wraps(api_func)
        def api_wrapper(*args, **kwargs):
            resp = api_func(*args, **kwargs)
            if int(resp.headers['Content-Length']) > 3:
                return resp
            else:
                abort(code)
        return api_wrapper
    return api_decorator


@api.route('/workouts', methods=['GET'])
@api.route('/workouts/<int:wid>', methods=['GET'])
@execute_or_abort(404)
def get_workout(wid=None):
    if wid is not None:
        results = Workout.query.filter_by(id=wid).first()
        if results is not None:
            results = [results]
        else:
            results = []
    else:
        results = Workout.query.all()
    return jsonify([wo.serialize() for wo in results])


@api.route('/workouts', methods=['POST', 'PUT'])
def add_workout():
    request.json['exercises'] = [Exercise(**kwargs) for kwargs in request.json['exercises']]
    wo = Workout(**request.json)
    db.session.add(wo)
    for e in request.json['exercises']:
        db.session.add(e)
    db.session.commit()
    return jsonify(wo.serialize())


@api.route('/workouts/<int:wid>', methods=['DELETE'])
@execute_or_abort(404)
def remove_workout(wid):
    resp = {}
    result = Workout.query.filter_by(id=wid).first()
    if result:
        db.session.delete(result)
        db.session.commit()
        resp['workout'] = result.serialize()
    return jsonify(resp)