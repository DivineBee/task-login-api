# Main BluePrint

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('project/index.html')


@main.route('/profile')
@login_required # prevents unauthorized access to the page
def profile():
    # current_user represents the user from the database
    # and provides access to all user's attributes with dot notation.
    return render_template('project/profile.html', name=current_user.name)
