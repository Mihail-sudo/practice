from flask import Blueprint, request, jsonify
from shop import db
from flask_login import current_user, login_required


api = Blueprint('api', __name__)

@api.route("/api")
def home():
    return 'Welcome home'
