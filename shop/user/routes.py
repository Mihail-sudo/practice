from flask import Blueprint
from flask_login import current_user, login_required, logout_user, login_user
from flask import redirect, url_for, flash, render_template, request
from shop import bcrypt, db
from shop.models import User, Product
from shop.user.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestPasswordForm, ResetPasswordForm
from shop.user.utils import safe_picture#, send_reset_email


user = Blueprint('user', __name__)


@user.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Acount created for {form.username.data}', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html', title='Registration', form=form)



@user.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@user.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            img_file = safe_picture(form.picture.data)
            current_user.image_file = img_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("You'r account has been updated!", 'success')
        return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', title='My account', 
                           image_file=image_file, form=form)
    

@user.route("/basket")
@login_required
def basket():
    products = Product.query.all()
    return render_template('basket.html', products=products)


@user.route('/reset_password')
def request_reset():
    pass
