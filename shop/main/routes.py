
from flask import Blueprint
from shop.models import Product#, User, Basket
from flask_login import current_user, login_required, logout_user, login_user
from flask import redirect, url_for, flash, render_template, request
from shop import bcrypt, db


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=10)
    return render_template('main.html', products=products)
