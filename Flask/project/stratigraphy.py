from flask import Blueprint, request, jsonify
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import json

stratigraphy = Blueprint('stratigraphy', __name__)


@stratigraphy.route('/process_data')
def process_data():
    with open('stratigraphy.json', 'r') as stratigraphy_file:
        stratigraphy_file = json.load(stratigraphy_file)
        print(stratigraphy_file)