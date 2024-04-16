from config import db
from Models.Carts import *
from Models.Products import *
from flask import request, jsonify
from datetime import datetime
from Services.Middleware import *


def add_to_cart():
    try:
        if request.method == 'POST':
            request_json = request.json

            product_id = request_json.get('product_id')
            amount = request_json.get('amount')
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

            if not product_id or not amount:
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
                if product.amount > amount:
                    cart_product.amount += amount
                    cart_product.total += product.price * amount
                    cart_product.price = product.price
                    cart_product.update_at = datetime.now()
                else:
                    return jsonify({
                        'status': 404,
                        'message': 'Amount in valid!'
                    }), 404

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


def settings_cart():
    try:
        request_json = request.json
        account_id = request_json.get('account_id')
        # # items = CartProducts.query.join(Cart).filter_by(account_id=account_id).all()
        # items = Cart.query.filter_by(account_id=account_id).all()
        #
        # records = []
        # for item in items.products:
        #     records.append({
        #         'product_id': item.product_id,
        #         'amount': item.amount,
        #         'price': item.price
        #     })
        # return jsonify({
        #     'test': records
        # }), 200
        cart = Cart.query.filter_by(account_id=account_id).first()
        if cart:
            # Serialize cart data to JSON
            cart_data = {
                'cart_id': cart.cart_id,
                'account_id': cart.account_id,
                'create_at': cart.create_at.isoformat(),
                'update_at': cart.update_at.isoformat(),
                'products': [],
                'x': []
            }
            for cart_product in cart.products:
                product_data = {
                    'product_id': cart_product.product_id,
                    'amount': cart_product.amount,
                    'price': cart_product.price,
                    'total': cart_product.amount * cart_product.price,
                    'create_at': cart_product.create_at.isoformat(),
                    'update_at': cart_product.update_at.isoformat()
                }
                cart_data['products'].append(product_data)

            # Query CartProducts associated with the cart
            cart_products = CartProducts.query.filter_by(cart_id=cart.cart_id).all()
            for cart_product in cart_products:
                product_data = {
                    'product_id': cart_product.product_id,
                    'amount': cart_product.amount,
                    'price': cart_product.price,
                    'total': cart_product.total,
                    'create_at': cart_product.create_at.isoformat(),
                    'update_at': cart_product.update_at.isoformat()
                }
                cart_data['x'].append(product_data)
            return jsonify(cart_data), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500
