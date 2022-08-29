from shop.user.utils import safe_picture
from flask import (Blueprint, render_template, request, 
                   redirect, url_for, flash, abort)
from flask_login import login_required, current_user
from shop.models import Product
from shop import db
from .forms import NewProductForm

product = Blueprint('product', __name__)


@product.route('/product/new', methods=['GET', 'POST'])
@login_required
def add_product():
    form = NewProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, subscribe=form.subscribe.data, image_file=form.img_file.data, author=current_user)
        db.session.add(product)
        db.session.commit()
        flash("Has been added", 'success')
        return redirect(url_for('main.home'))
    return render_template('add_product.html', title='New product', form=form, legend='New product')

@product.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_info(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', title=product.name)


@product.route('/product/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Product.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = NewProductForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update post', form=form, legend='Update post')


@product.route('/product/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Product.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted', 'success')
    return redirect(url_for('main.home'))