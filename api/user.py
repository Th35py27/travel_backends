import json, jwt
from flask import Flask, Blueprint, request, jsonify, current_app, Response, make_response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        #@token_required
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            print(body)
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2     acters'}, 400
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            password = body.get('password')
            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(name=name, uid=uid)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                print(user.read())
                return ((user.read()), 200)
            # failure returns error
            return make_response({'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400)

        @token_required
        def get(self, current_user): # Read Method
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        
        @token_required
        def delete(self, current_user):
            body = request.get_json()
            uid = body.get('uid')
            users = User.query.all()
            for user in users:
                if user.uid == uid:
                    user.delete()
            return jsonify(user.read())
        
        @token_required
        def put(self, current_user):
            body = request.get_json() # get the body of the request
            uid = body.get('uid') # get the UID (Know what to reference)
            name = body.get('name')
            users = User.query.all()
            for user in users:
                if user.uid == uid:
                    user.update(name,'','')
            return f"{user.read()} Updated"
    
    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                print(body)
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                ''' Get Data '''
                uid = body.get('uid')
                if uid is None:
                    print("error at uid")
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')
                
                ''' Find user '''
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    print("error at password")
                    return {'message': f"Invalid user id or password"}, 400
                if user:
                    try:
                        token = jwt.encode(
                            {"_uid": user._uid},
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie(key="jwt", value=token, max_age=3600, secure=False, samesite='None', path='/', httponly=False)
                        print(resp.headers)
                        return resp
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500

            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')