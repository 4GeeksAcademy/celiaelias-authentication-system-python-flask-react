"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS, cross_origin
from flask_jwt_extended import create_access_token, JWTManager
#import hash_function

api = Blueprint('api', __name__)
#api.config["JWT_SECRET_KEY"] = "super-secret" 
#jwt = JWTManager(api)

# Allow CORS requests to this API
CORS(api, methods=["GET", "POST", "PUT"])

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/sign_up', methods=['POST'])
def manage_sign_up():
    print('hola')
    request_data = request.get_json()
    print(request_data)

    if not 'email' in request_data:
        return jsonify({"error": "The email is not present"}), 400
    
    if not('password' in request_data) or not('passwordConfirmation' in request_data):
        return jsonify({"error": "The password or password confirmation is not present"}), 400

    email = request_data['email']
    password = request_data['password']
    password_confirmation = request_data['passwordConfirmation']

    if password != password_confirmation:
        return jsonify({"error": "Please verify that password is equal to your password confirmation field"}), 400
    #password = hash_function(request_data['password'])

    user = User(email=email, password=password, is_active=True)
    db.session.add(user)
    db.session.commit() 

    response_body = {
        "message": "The user was created without problem "
    }

    return jsonify(response_body), 200

@cross_origin()  # Agrega el decorador cross_origin aquí
@api.route("/sign_in", methods=["POST"])
def sign_in():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    #return jsonify({"msg": "test"})

    user = User.query.filter_by(email=email,password=password).one_or_none()
    
    if user:
        user_data = {
            "id": user.id,
            "email": user.email,
        }
        #return(jsonify(user_data))
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
       # return jsonify(user_data)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

    #if not user or not user.check_password(password):
    #    return jsonify("Wrong username or password"), 401

    # Notice that we are passing in the actual sqlalchemy user object here


@api.route('/profile', methods=['GET'])
def profile():
    print("profile")