from flask import Blueprint
from shop.models import Product, User#, Basket
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


@login_required
@main.route("/buy/<int:product_id>", methods=["POST", "GET"])
def buy(product_id):
    product = Product.query.get(product_id)
    user = User.query.get(current_user.id)
    product.clients.append(user)
    db.session.add(product)
    # product = Product.query.get(product_id)
    # user = User.query.with_parent(product).all()
    db.session.commit()
    print(product, user)
    return redirect(url_for('main.home'))
