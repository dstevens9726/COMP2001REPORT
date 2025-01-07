from flask import Flask, request, jsonify, session
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from functools import wraps
from flask_session import Session
import requests
from datetime import timedelta
import callProcedures
from __init__ import app
from verifyUser import token_required, role_required, SECRET_KEY


CORS(app)  # Allow cross-origin requests (important for Swagger)

# Initialize Swagger UI via Flask-RESTX
api = Api(
    app,
    version='1.0',
    title='COMP2001 Trail app Microservice by Dan',
    description='API enabling trail application to function by providing the ability to manage users, features, and trails',
    doc='/swagger',  # Swagger UI will be accessible at this path
    security='BearerAuth'
)
api.authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
    }
}



health_ns = api.namespace('Health', description='Health Check for Server')

@health_ns.route('/ping')
class Ping(Resource):
    @api.doc(description="Ping the server to check its status")
    @api.response(200, "Success", example={"message": "pong"})
    def get(self):
        """Returns a pong response to confirm the server is running"""
        return {"message": "pong"}, 200

users_ns = api.namespace('Users', description='User operations')
trails_ns = api.namespace('Trails', description='Trail operations')
feature_ns = api.namespace('Feature', description='Feature operations')
trail_feature_ns = api.namespace('Trail Feature', description='Trail Feature operations')
login_ns = api.namespace('login', description='login operations')

user_model = api.model('User', {
    'UserName': fields.String(required=True, description='The users name'),
    'UserEmail': fields.String(required=True, description='The users email address'),
    'Password': fields.String(required=True, description='The users password'),
    'Role': fields.String(required=True, description='The role of the user'),
})

trail_model = api.model('Trail', {
    'TrailName': fields.String(required=True, description='The name of the trail'),
    'TrailSummary': fields.String(required=True, description='A summary of the trail'),
    'TrailDescription': fields.String(required=True, description='A description of the trail'),
    'Difficulty': fields.String(required=True, description='The trails difficulty'),
    'Location': fields.String(required=True, description='The location of the trail'),
    'Length': fields.Float(required=True, description='The distance of the trail in kilometers'),
    'ElevationGain': fields.Float(required=True, description='The elevation gain of the trail in meters'),
    'RouteType': fields.String(required=True, description='The type of route'),
    'OwnerID': fields.Integer(required=True, description='The user ID of the trail owner'),
    'Pt1_Lat': fields.Float(required=True, description='Latitude of Point 1'),
    'Pt1_Long': fields.Float(required=True, description='Longitude of Point 1'),
    'Pt1_Desc': fields.String(required=True, description='Description of Point 1'),
    'Pt2_Lat': fields.Float(required=True, description='Latitude of Point 2'),
    'Pt2_Long': fields.Float(required=True, description='Longitude of Point 2'),
    'Pt2_Desc': fields.String(required=True, description='Description of Point 2'),
    'Pt3_Lat': fields.Float(required=True, description='Latitude of Point 3'),
    'Pt3_Long': fields.Float(required=True, description='Longitude of Point 3'),
    'Pt3_Desc': fields.String(required=True, description='Description of Point 3'),
    'Pt4_Lat': fields.Float(required=True, description='Latitude of Point 4'),
    'Pt4_Long': fields.Float(required=True, description='Longitude of Point 4'),
    'Pt4_Desc': fields.String(required=True, description='Description of Point 4'),
    'Pt5_Lat': fields.Float(required=True, description='Latitude of Point 5'),
    'Pt5_Long': fields.Float(required=True, description='Longitude of Point 5'),
    'Pt5_Desc': fields.String(required=True, description='Description of Point 5'),
})

feature_model = api.model('Feature', {
    'TrailFeature': fields.String(required=True, description='The name of the feature'),
})

trail_feature_model = api.model('Trail Feature', {
    'TrailID': fields.Integer(required=True, description='The id of the Trail'),
    'FeatureID': fields.Integer(required=True, description='The id of the Feature')
    
})
                               

login_model = api.model('Login', {
    'email': fields.String(required=True, description='The email of the user'),
    'password': fields.String(required=True, description='The password of the user'),
})

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = SECRET_KEY  
Session(app)

AUTH_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

@login_ns.route('/login')
class Login(Resource):
    @login_ns.doc('user_login')
    @login_ns.expect(login_model)
    def post(self):
        """Authenticate user with the Authentication API and create a session for API access"""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'message': 'Email and password required'}, 400

        try:
            response = requests.post(
                AUTH_API_URL,
                json={"email": email, "password": password},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                try:
                    auth_response = response.json()
                    if isinstance(auth_response, list) and len(auth_response) >= 2 and auth_response[0] == "Verified":
                        verified_status = auth_response[1]

                        # Store the user's data in session
                        session['email'] = email
                        session['role'] = 'Admin' if verified_status == "True" else 'User'

                        return {
                            "message": "Login successful",
                            "verified": verified_status == "True",
                            "role": session['role']
                        }, 200

                    else:
                        return {"message": "Unexpected API response", "response_content": auth_response}, 500

                except ValueError:
                    return {"message": "Invalid JSON response from Authenticate API"}, 500

            else:
                return {
                    "message": f"Authentication failed with status code {response.status_code}",
                    "response_text": response.text
                }, response.status_code

        except requests.RequestException as e:
            return {"message": f"Error connecting to Authenticate API: {str(e)}"}, 500


@users_ns.route('')
class Users(Resource):
    @users_ns.doc('get_all_users')
    def get(self):
        """Get all users details"""
        return callProcedures.get_all_users()

    @users_ns.expect(user_model)
    @users_ns.doc('create_user')
    def post(self):
        """Create a new User"""
        return callProcedures.add_user()

@users_ns.route('/<string:user_id>')
@users_ns.param('user_id', 'The users ID')
class User(Resource):
    @users_ns.doc('get_user_by_id', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def get(self, user_id):
        """Fetch a specific User """
        return callProcedures.get_user_by_id(user_id)

    @users_ns.expect(user_model)
    @users_ns.doc('update_user', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def put(self, user_id):
        return callProcedures.edit_user(user_id)

    @users_ns.doc('delete_user', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def delete(self, user_id):
        return callProcedures.remove_user(user_id)


@trails_ns.route('/')
class Trails(Resource):
    @trails_ns.doc('get_all_trails')
    def get(self):
        """Fetch all trails"""
        return callProcedures.get_all_trails()

    @trails_ns.expect(trail_model)
    @trails_ns.doc('create_trail', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def post(self):
        """Create a new trail"""
        return callProcedures.add_trail()

@trails_ns.route('/<string:TrailID>')
@trails_ns.param('TrailID', 'The Trail ID')
class Trail(Resource):
    @trails_ns.doc('delete_trail', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def delete(self, TrailID):
        """Delete a trail by its ID"""
        return callProcedures.remove_trail(TrailID)

    @trails_ns.expect(trail_model)
    @trails_ns.doc('update_trail', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def put(self, TrailID):
        """Update a trail using its ID"""
        return callProcedures.edit_trail(TrailID)

    @trails_ns.doc('fetch_trail_by_id', security='BearerAuth')
    def get(self, TrailID):
        """Fetch a specific trail using its ID"""
        return callProcedures.get_trail_by_id(TrailID)


@feature_ns.route('/')
class Feature(Resource):

    @feature_ns.doc('get_all_features')
    def get(self):
        """Fetch all features"""
        return callProcedures.fetch_all_features()

    @feature_ns.expect(feature_model)
    @feature_ns.doc('create_feature', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def post(self):
        """Create a new feature"""
        return callProcedures.create_feature()

@feature_ns.route('/<string:feature_id>')
@feature_ns.param('feature_id', 'The feature ID')
class Feature(Resource):
    @feature_ns.doc('get_feature_by_id')
    def get(self, feature_id):
        """Get specific feature using its ID"""
        return callProcedures.fetch_feature_by_id(feature_id)

    @feature_ns.expect(feature_model)
    @feature_ns.doc('update_feature', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def put(self, feature_id):
        """Update a feature using its ID """
        return callProcedures.update_feature(feature_id)

    @feature_ns.doc('delete_feature', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def delete(self, feature_id):
        """Delete a feature using its ID """
        return callProcedures.delete_feature(feature_id)

@trail_feature_ns.route('/')
class TrailFeature(Resource):

    @trail_feature_ns.doc('get_all_trail_features')
    def get(self):
        """Fetch all trail features"""
        return callProcedures.fetch_all_trail_features()

    @trail_feature_ns.expect(trail_feature_model)
    @trail_feature_ns.doc('create_trail_feature', security='BearerAuth')
    @token_required
    @role_required('Admin')
    def post(self):
        """Create a new trail feature"""
        return callProcedures.create_trail_feature()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
