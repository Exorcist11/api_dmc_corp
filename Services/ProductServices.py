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
            products_data = []
            for product in products:
                products_data.append({
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
                'list_product': products_data
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
