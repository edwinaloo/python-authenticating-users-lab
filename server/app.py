from flask import Flask, request, jsonify, session
from flask_restful import Api, Resource

app = Flask(__name__)
app.secret_key = 'your_secret_key'
api = Api(app)


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        
        # Retrieve the user by username (assuming you have a user database)
        user = get_user_by_username(username)
        
        if user:
            # Set the session's user_id value to the user's id
            session['user_id'] = user.id
            return jsonify(user), 200
        else:
            return {'message': 'Invalid username'}, 401


class LogoutResource(Resource):
    def delete(self):
        if 'user_id' in session:
            # Remove the user_id value from the session
            session.pop('user_id')
        
        return '', 204


class CheckSessionResource(Resource):
    def get(self):
        if 'user_id' in session:
            # Return the user as JSON with a 200 status code
            user_id = session['user_id']
            user = get_user_by_id(user_id)
            return jsonify(user), 200
        else:
            return '', 401


api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(CheckSessionResource, '/check_session')

if __name__ == '__main__':
    app.run(port=5555)