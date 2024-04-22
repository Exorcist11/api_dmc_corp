from config import db
from Models.Carts import *
from Models.Products import *
from Models.Images import Image
from Models.Orders import *
from flask import request, jsonify
from datetime import datetime
from Services.Middleware import *


def add_to_cart():
    try:
        if request.method == 'POST':
            request_json = request.json

            product_id = request_json.get('product_id')
            amount = request_json.get('amount', 1)
            account_id = request_json.get('account_id')

            cart = Cart.query.filter_by(account_id=account_id).first()
            if not cart:
                new_cart = Cart(
                    cart_id=generate_custom_id('CART'),
                    account_id=account_id
                )
                db.session.add(new_cart)
                db.session.commit()

                cart = Cart.query.filter_by(account_id=account_id).first()

            if not product_id:
                return jsonify({
                    'status': 400,
                    'message': 'Missing required fields!'
                }), 400

            product = Product.query.filter_by(product_id=product_id).first()

            if not product:
                return jsonify({
                    'status': 404,
                    'message': 'Product not found!'
                }), 404

            cart_product = CartProducts.query.filter_by(cart_id=cart.cart_id, product_id=product_id).first()
            if cart_product:
                if cart_product.amount == product.amount:
                    cart_product.amount = product.amount
                    cart_product.total = product.price * product.amount
                    cart_product.update_at = datetime.now()
                    return jsonify({
                        'status': 429,
                        'message': 'Exceed the limit'
                    }), 429
                else:
                    cart_product.amount += amount
                    cart_product.total += product.price * amount
                    cart_product.update_at = datetime.now()

            else:
                cart_product = CartProducts(
                    cart_id=cart.cart_id,
                    product_id=product_id,
                    amount=amount,
                    total=amount * product.price,
                    price=product.price
                )
                db.session.add(cart_product)
            db.session.commit()

            return jsonify({
                'status': 200,
                'message': 'Add product to cart success'
            }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def settings_cart(account_id):
    try:
        if request.method == 'GET':
            cart = Cart.query.filter_by(account_id=account_id).first()
            total = 0
            if cart:
                cart_data = {
                    'cart_id': cart.cart_id,
                    'account_id': cart.account_id,
                    'create_at': cart.create_at.isoformat(),
                    'update_at': cart.update_at.isoformat(),
                    'product': [],
                    'cart_total': total
                }

                cart_products = CartProducts.query.filter_by(cart_id=cart.cart_id).all()
                for cart_product in cart_products:
                    total = total + cart_product.total
                    product_info = Product.query.filter_by(product_id=cart_product.product_id).first()
                    images = Image.query.filter_by(product_id=cart_product.product_id).all()
                    image_url = [image.url for image in images]

                    product_data = {
                        'product_id': cart_product.product_id,
                        'product_name': product_info.product_name,
                        'amount': cart_product.amount,
                        'price': cart_product.price,
                        'category': product_info.category.category_name,
                        'size': product_info.size,
                        'total': cart_product.total,
                        'image': image_url[0],
                        'total_product': product_info.amount,
                        'create_at': cart_product.create_at.isoformat(),
                        'update_at': cart_product.update_at.isoformat()
                    }
                    cart_data['product'].append(product_data)
                    cart_data['cart_total'] = total

                return jsonify(cart_data), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def remove_product_from_cart():
    try:
        request_json = request.json

        product_id = request_json.get('product_id')
        cart_id = request_json.get('cart_id')

        cart_product = CartProducts.query.filter_by(cart_id=cart_id, product_id=product_id).first()
        if not cart_product:
            return jsonify({
                'status': 200,
                'message': 'Product in cart not found'
            }), 404

        if request.method == 'PATCH':
            if cart_product.amount > 1:
                cart_product.amount -= 1
                cart_product.total = cart_product.total - cart_product.price
                cart_product.update_at = datetime.now()
            else:
                db.session.delete(cart_product)
            db.session.commit()

            return jsonify({
                'status': 200,
                'message': "Update cart success",
            }), 200

        if request.method == 'POST':
            db.session.delete(cart_product)
            db.session.commit()

            return jsonify({
                'status': 200,
                'message': 'Delete item success'
            }), 200
            pass
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500



