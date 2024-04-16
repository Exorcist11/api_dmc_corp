from Models.Users import User
from Models.Accounts import Account
from Models.Roles import Role
from Models.News import New
from Models.Address import Address
from Models.Sellers import Seller
from Models.Products import Product
from Models.Categories import Category
from Models.Images import Image
from Models.Reviews import Review
from Models.Carts import Cart, CartProducts
from Models.Orders import OrderProduct, Order
from Models.WishList import WishList

from config import db, app

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
