from flask import Blueprint, request, jsonify
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Incorrect credentials'}), 401  # unauthorized
    else:
        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)

        return jsonify({
            'user': {
                'refresh': refresh,
                'access': access,
                'username': user.username,
                'email': user.email
            }
        }), 200  # ok


# part of validation and adding user to db
@auth.route('/signup', methods=['POST'])
def signup():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    # get the user email/username if that already exists via filtering
    is_user_email = User.query.filter_by(email=email).first()
    is_user_username = User.query.filter_by(email=email).first()
    # hash the password using 'sha' (bad practice saving in plain-text)
    password_sha = generate_password_hash(password, method='sha256')

    # Validating user input
    if len(password) < 6:
        return jsonify({'error': 'Password is too short'}), 400  # bad request

    if len(username) < 3:
        return jsonify({'error': 'Username is too short'}), 400

    if not username.isalnum() or " " in username:
        return jsonify({'error': 'Username should be alphanumeric, with no spaces'}), 400

    if not validators.email(email):
        return jsonify({'error': 'Email is not valid'}), 400

    if is_user_email:
        return jsonify({'error': 'Email address already exists'}), 409  # conflict

    if is_user_username:
        return jsonify({'error': 'Username already exists'}), 409

    # create user with the input provided
    user = User(email=email, username=username, password=password_sha)

    # add user to db
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created',
        'user': {
            'username': username, 'email': email
        }
    }), 201


@auth.route('/profile')
@jwt_required()  # doesn't make sense to logout if the user is not logged in
def profile():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    return jsonify({
        'username': user.username,
        'email': user.email,
    }), 200


@auth.route('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)
    return jsonify({
        'access': access,
    }), 200