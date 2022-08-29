#from email.policy import default
from email.policy import default
from itsdangerous import URLSafeTimedSerializer as Serializer

from shop import db, login_manager
from flask import current_app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# class Basket(db.Model):
#     __tablename__ = 'basket'
#     client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, primary_key=True)
#     count = db.Column(db.Integer, nullable=False, default=1)
    

basket = db.Table(
    'basket',
    db.Column('client_id', db.ForeignKey('user.id'), primary_key=True),
    db.Column('product_id', db.ForeignKey('product.id'), primary_key=True),
    db.Column('count', db.Integer, nullable=False, default=1),
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='user.png')
    password = db.Column(db.String(60), nullable=False)
    
    posted_product = db.relationship('Product', backref='author', lazy=True)
    
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token, expires_sec)['user_id']
        except:  
            return None
        return User.query.get(user_id)
    
    def __repr__(self) -> str:
        return f'User {self.username}, {self.email}, {self.image_file}'
    

class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    subscribe = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='')
    
    clients = db.relationship('User', secondary=basket, backref="products")
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
