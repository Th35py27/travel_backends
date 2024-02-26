from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building

from model.activities import Activity

# Change variable name and API name and prefix
activity_api = Blueprint('activity_api', __name__,
                   url_prefix='/api/activity')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(activity_api)

class ActivityAPI:     
    class Action(Resource):
        def get(self):
            # Querying the database to retrieve all rows and specified columns
            data = Activity.query.with_entities(
                Activity.activity,
                Activity.family,
                Activity.adult,
                Activity.indoors,
                Activity.outdoors
            ).all()

            # Transforming the query result into a list of dictionaries
            result = [
                {
                    "activity": row.activity,
                    "family": row.family,
                    "adult": row.adult,
                    "indoors": row.indoors,
                    "outdoors": row.outdoors
                }
                for row in data
            ]

            return jsonify(result)


    # building RESTapi endpoint, method distinguishes action
    api.add_resource(Action, '/')
