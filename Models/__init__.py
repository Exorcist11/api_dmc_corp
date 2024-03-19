from Users import User
from Accounts import Account
from Roles import Role
from News import New
from Address import Address
from Sellers import Seller
from Products import Product
from Categories import Category, CategoryProduct
from Images import Image
from Reviews import Review
from Carts import Cart, CartProducts
from Orders import OrderProduct, Order

from config import db, app

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
