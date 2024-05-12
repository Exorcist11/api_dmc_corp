from config import *
from Models.Carts import *
from Models.Products import *
from Models.Images import Image
from Models.Address import *
from Models.Users import *
from Models.Orders import *
from Models.Reviews import *
from flask import request, jsonify
from datetime import datetime
from Services.Middleware import *


def cart_checkout():
    try:
        request_json = request.json
        cart_id = request_json.get('cart_id')
        account_id = request_json.get('account_id')
        address_id = request_json.get('address_id')
        payment = request_json.get('payment')
        cart_product = CartProducts.query.filter_by(cart_id=cart_id).all()
        order_id = generate_custom_id('ORDER')

        new_order = Order(
            order_id=order_id,
            account_id=account_id,
            payment=payment,
            note='',
            address_id=address_id,
            total=0
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

        if order_product.total < 700000:
            order_product.total += 30000

        db.session.commit()

        # user = User.query.filter_by(account_id=account_id).first()
        # msg = Message('Đơn hàng đã đặt thành công!', sender=user.email, recipients=['demokahootft@gmail.com'])
        # html = f"""
        #     <!doctype html>
        #     <html>
        #       <head>
        #         <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        #       </head>
        #       <body style="font-family: sans-serif;">
        #         <div style="display: block; margin: auto; max-width: 600px;" class="main">
        #           <h1 style="font-size: 18px; font-weight: bold; margin-top: 20px">
        #             Đơn hàng của bạn đã được đặt thành công!
        #           </h1>
        #           <p>Mã đơn hàng - {order_id} </p>
        #           <p>Inspect it using the tabs you see above and learn how this email can be improved.</p>
        #           <img alt="Inspect with Tabs" src="cid:welcome.png" style="width: 100%;">
        #           <p>Now send your email using our fake SMTP server and integration of your choice!</p>
        #           <p style="color: red">Good luck! Hope it works.</p>
        #         </div>
        #
        #       </body>
        #     </html>
        #     """
        #
        # msg.html = html
        # mail.send(msg)

        return jsonify({
            'status': 200,
            'message': 'Order success',
            'order_id': order_id
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
        elif status == 'completed':
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
        orders = Order.query.order_by(Order.create_at.desc()).all()
        record = []
        for order in orders:
            record.append({
                'order_id': order.order_id,
                'status': order.status,
                'payment': order.payment,
                'total': order.total,
                'create_at': order.create_at.strftime("%H:%M:%S %d/%m/%Y")
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


def get_order_pending():
    try:
        orders = Order.query.filter_by(status='pending').order_by(Order.create_at.desc()).all()
        record = []
        for order in orders:
            record.append({
                'order_id': order.order_id,
                'status': order.status,
                'payment': order.payment,
                'total': order.total,
                'create_at': order.create_at.strftime("%H:%M:%S %d/%m/%Y")
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
            'create_at': order.create_at.strftime("%H:%M:%S %d/%m/%Y"),
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
                'warehouse': product.amount,
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
        orders = Order.query.filter_by(account_id=account_id).order_by(Order.create_at.desc()).all()

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


def review_by_customer():
    try:
        request_json = request.json
        order_id = request_json.get('order_id')
        product_id = request_json.get('product_id')
        title = request_json.get('title')
        content = request_json.get('content')
        rate = request_json.get('rate', None)

        order = Order.query.filter_by(order_id=order_id).first()

        if order.status == 'completed':
            review = Review.query.filter_by(order_id=order_id, account_id=order.account_id, product_id=product_id).first()
            if review is None:
                new_review = Review(
                    title=title,
                    content=content,
                    rate=rate,
                    order_id=order_id,
                    product_id=product_id,
                    account_id=order.account_id
                )
                db.session.add(new_review)
                db.session.commit()

                return jsonify({
                    'status': 200,
                    'message': 'New rating product'
                }), 200
        else:
            return jsonify({
                'status': 402,
                'message': 'Order not completed'
            }), 402

    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_product_by_user_bought(account_id):
    try:
        orders = Order.query.filter_by(account_id=account_id).all()
        record = []
        for order in orders:
            products = OrderProduct.query.filter_by(order_id=order.order_id).all()
            for item in products:
                product = Product.query.filter_by(product_id=item.product_id).first()
                images = Image.query.filter_by(product_id=item.product_id).all()
                image_url = [image.url for image in images]
                record.append({
                    'product_id': item.product_id,
                    'product_name': product.product_name,
                    'path_product': product.path_product,
                    'size': product.size,
                    'material': product.material,
                    'color': product.color,
                    'width': product.width,
                    'category': product.category.category_name,
                    'seller': product.seller.seller_name,
                    'time': order.create_at.strftime("%H:%M:%S %d-%m-%Y"),
                    'image': image_url[0]
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


def get_order_pending():
    try:
        orders = Order.query.filter_by(status='pending').order_by(Order.create_at.desc()).all()
        record = []
        for order in orders:
            record.append({
                'order_id': order.order_id,
                'status': order.status,
                'payment': order.payment,
                'total': order.total,
                'create_at': order.create_at.strftime("%H:%M:%S %d/%m/%Y")
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
