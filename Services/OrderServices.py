from config import db
from Models.Carts import *
from Models.Products import *
from Models.Images import Image
from Models.Address import *
from Models.Orders import *
from flask import request, jsonify
from datetime import datetime
from Services.Middleware import *


def cart_checkout():
    try:
        request_json = request.json
        cart_id = request_json.get('cart_id')
        account_id = request_json.get('account_id')
        address_id = request_json.get('address_id')
        cart_product = CartProducts.query.filter_by(cart_id=cart_id).all()
        order_id = generate_custom_id('ORDER')

        new_order = Order(
            order_id=order_id,
            account_id=account_id,
            payment='cash',
            note='',
            address_id=address_id,
            total=100
        )
        db.session.add(new_order)
        order_product = Order.query.filter_by(order_id=order_id).first()

        for item in cart_product:
            product = Product.query.filter_by(product_id=item.product_id).first()
            order_detail = OrderProduct(
                order_id=order_id,
                product_id=item.product_id,
                amount=item.amount,
                price=item.price
            )
            order_product.total += item.amount * item.price
            db.session.add(order_detail)

            if product.amount > item.amount:
                product.amount = product.amount - item.amount
                cart_info = CartProducts.query.filter_by(cart_id=cart_id, product_id=item.product_id).first()
                db.session.delete(cart_info)
            else:
                return jsonify({
                    'status': 404,
                    'message': 'Item not valid!'
                }), 404

        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Order success'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def active_order():
    try:
        request_json = request.json
        status = request_json.get('status')
        order_id = request_json.get('order_id')
        order = Order.query.filter_by(order_id=order_id).first()
        if status == 'active':
            order.status = status
        elif status == 'finish':
            order.status = status
        elif status == 'reject':
            order_product = OrderProduct.query.filter_by(order_id=order_id).all()
            order.status = status
            for item in order_product:
                product = Product.query.filter_by(product_id=item.product_id).first()
                product.amount += item.amount
                product.update_at = datetime.now()
        order.update_at = datetime.now()
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': f'Order {status}'
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_order():
    try:
        orders = Order.query.all()
        record = []
        for order in orders:
            record.append({
                'order_id': order.order_id,
                'status': order.status,
                'payment': order.payment,
                'total': order.total,
                'create_at': order.create_at
            })
        return jsonify({
            'status': 200,
            'record': record
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_order_detail(order_id):
    try:
        order = Order.query.filter_by(order_id=order_id).first()

        address = Address.query.filter_by(address_id=order.address_id).first()
        address_detail = {
            'full_name': address.full_name,
            'phone_number': address.phone_number,
            'note': address.note,
            'province': get_province(address.province),
            'district': get_district(address.district),
            'ward': get_ward(address.ward)
        }

        order_detail = {
            'order_id': order.order_id,
            'account_id': order.account_id,
            'status': order.status,
            'payment': order.payment,
            'note': order.note,
            'total': order.total,
            'address': address_detail,
            'product': []
        }

        order_product = OrderProduct.query.filter_by(order_id=order_id).all()
        for item in order_product:
            product = Product.query.filter_by(product_id=item.product_id).first()
            images = Image.query.filter_by(product_id=item.product_id).all()
            image_url = [image.url for image in images]
            
            order_detail['product'].append({
                'product_id': item.product_id,
                'product_name': product.product_name,
                'amount': item.amount,
                'price': product.price,
                'category': product.category.category_name,
                'size': product.size,
                'image': image_url[0],
                'order_total': item.amount * product.price
            })

        return jsonify({
            'status': 200,
            'order': order_detail
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_order_by_action(status):
    try:
        orders = Order.query.filter_by(status=status).all()
        record = []
        for order in orders:
            record.append({
                'order_id': order.order_id,
                'account_id': order.account_id,
                'status': order.status,
                'payment': order.payment,
                'note': order.note,
                'total': order.total,
                'create_at': order.create_at,
                'update_at': order.update_at
            })
        return jsonify({
            'status': 200,
            'record': record
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_order_by_account(account_id):
    try:
        orders = Order.query.filter_by(account_id=account_id).all()

        record = []
        for order in orders:
            amount_item = OrderProduct.query.filter_by(order_id=order.order_id).count()
            record.append({
                'order_id': order.order_id,
                'account_id': order.account_id,
                'status': order.status,
                'payment': order.payment,
                'note': order.note,
                'total': order.total,
                'quantity': amount_item,
                'create_at': order.create_at.strftime("%H:%M:%S %d/%m/%Y"),
                'update_at': order.update_at.strftime("%H:%M:%S %d-%m-%Y")
            })
        return jsonify({
            'status': 200,
            'record': record
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500
