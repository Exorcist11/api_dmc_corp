from Models.Products import Product
from flask import request, jsonify
from config import db


def manage_product():
    try:
        request_form = request.json
        if request.method == 'POST':
            new_product = Product(
                product_id=request_form['product_id'],
                product_name=request_form['product_name'],
                seller_id=request_form['seller'],
                category_id=request_form['category_id'],
                price=request_form.get('price', None),
                amount=request_form.get('amount', None),
                color=request_form.get("color", None),
                material=request_form.get('material', None),
                size=request_form.get('size', None),
                width=request_form.get('width', None),
                waterproof=request_form.get('waterproof', None),
                description=request_form.get('description', None)
            )
            db.session.add(new_product)
            db.session.commit()

            return jsonify({
                'status': 200,
                'message': 'ADD SUCCESSFULLY'
            })

        if request.method == 'GET':
            products = Product.query.all()
            record = []
            for product in products:
                record.append({
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'seller_name': product.seller.seller_name,
                    'nation': product.seller.nation,
                    'price': product.price,
                    'amount': product.amount,
                    'rate': product.rate,
                    'color': product.color,
                    'material': product.material,
                    'size': product.size,
                    'width': product.width,
                    'waterproof': product.waterproof,
                    'description': product.description
                })
            return jsonify({
                'status': 200,
                'list_product': record
            }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def setting_product(product_id):
    try:
        product = Product.query.filter_by(product_id=product_id).first_or_404()
        request_json = request.json

        if request.method == 'GET':
            info_product = {
                'product_name': product.product_name,
                'seller_name': product.seller.seller_name,
                'nation': product.seller.nation,
                'price': product.price,
                'amount': product.amount,
                'rate': product.rate,
                'color': product.color,
                'material': product.material,
                'size': product.size,
                'width': product.width,
                'waterproof': product.waterproof,
                'description': product.description
            }
            return jsonify({
                'status': 200,
                'product': info_product,
                'message': 'INFOR PRODUCT'
            })
        if request.method == 'PATCH':
            product.product_id = request_json['product_id'],
            product.product_name = request_json['product_name'],
            product.seller_id = request_json['seller'],
            product.category_id = request_json['category_id'],
            product.price = request_json.get('price', None),
            product.amount = request_json.get('amount', None),
            product.color = request_json.get("color", None),
            product.material = request_json.get('material', None),
            product.size = request_json.get('size', None),
            product.width = request_json.get('width', None),
            product.waterproof = request_json.get('waterproof', None),
            product.description = request_json.get('description', None)

            after = Product.query.filter_by(product_id=product_id).first_or_404()
            info_product = {
                'product_name': after.product_name,
                'seller_name': after.seller.seller_name,
                'nation': after.seller.nation,
                'price': after.price,
                'amount': after.amount,
                'rate': after.rate,
                'color': after.color,
                'material': after.material,
                'size': after.size,
                'width': after.width,
                'waterproof': after.waterproof,
                'description': after.description
            }
            return jsonify({
                'satus': 200,
                'message': 'SUCCESS',
                'product': info_product
            }), 200

        if request.method == 'DELETE':
            db.session.delete(product)
            db.session.commit()

            return jsonify({
                'satus': 200,
                'message': 'DELETE SUCCESS',
            }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_product_by_seller(seller_id):
    try:
        if request.method == 'GET':
            products = Product.query.filter_by(seller_id=seller_id).all()
            list_product = []
            for product in products:
                list_product.append({
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'seller_name': product.seller.seller_name,
                    'nation': product.seller.nation,
                    'price': product.price,
                    'amount': product.amount,
                    'rate': product.rate,
                    'color': product.color,
                    'material': product.material,
                    'size': product.size,
                    'width': product.width,
                    'waterproof': product.waterproof,
                    'description': product.description
                })
            return jsonify({
                'status': 200,
                'list_product': list_product
            }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_best_product():
    try:
        return True
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500
