from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.activities import Activity

# Change variable name and API name and prefix
activity_api = Blueprint('activity_api', __name__,
                   url_prefix='/api/activity')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(activity_api)

class ActivityAPI:     
    class _Read(Resource):
        def get(self):
            activities = Activity.query.all()
            json_ready = [activity.read() for activity in activities]
            return jsonify(json_ready)

    # building RESTapi endpoint, method distinguishes action
    api.add_resource(_Read, '/')
