from app import db, login
from flask_login import UserMixin #IS ONLY USED FOR THE USER MODEL!!!!!!!!
from datetime import datetime as dt 
from werkzeug.security import generate_password_hash, check_password_hash


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    # icon = db.Column(db.Integer)
    item = db.relationship('Item',
                    secondary = 'cart',
                    backref='users',
                    lazy='dynamic',
                    ) 

    # should return a unique identifying string
    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'

    # human readable version of rpr
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    # salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email=data['email']
        self.password = self.hash_password(data['password'])
    
    def save(self):
        db.session.add(self)  #adds the user to the db session
        db.session.commit() #save everything in the session to the db
    
    def add_item(self, item):
        self.item.append(item)
        db.session.commit()

    def remove_item(self, item):
        self.item.remove(item)
        db.session.commit()

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
        # SELECT  * FROM user WHERE id = ???


class Category(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    products = db.relationship('Item', backref="cat", 
                lazy="dynamic", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Category: {self.id}|{self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def from_dict(self,data):
            self.name = data['name']
            self.products = data['products']
        

class Item(db.Model):
    item_id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    desc = db.Column(db.Text)
    price = db.Column(db.Float)
    img=db.Column(db.String)
    created_on=db.Column(db.DateTime, index=True, default=dt.utcnow)
    category_id=db.Column(db.ForeignKey('category.id'))
    
    def __repr__(self):
        return f'<Item: {self.id}|{self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def from_dict(self, data):
        for field in ['name','desc','price','img','category_id']:
            if field in data:
                    #the object, the attribute, value
                setattr(self, field, data[field])
