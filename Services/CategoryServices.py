from Models.Categories import Category
from Models.Products import Product
from flask import jsonify, request
from config import db
from Services.Middleware import *


def manage_category():
    try:
        if request.method == 'GET':
            categories = Category.query.all()
            record = []
            for category in categories:
                record.append({
                    'category_id': category.category_id,
                    'category_name': category.category_name,
                })
            return jsonify({
                'status': 200,
                'record': record,
                'message': 'LIST CATEGORIES'
            }), 200

        if request.method == 'POST':
            new_category = Category(
                category_name=request.json.get('category_name'),
                path_category=convert_to_ascii(request.json.get('category_name'))
            )
            db.session.add(new_category)
            db.session.commit()

            return jsonify({
                'status': 200,
                'message': 'ADD SUCCESSFULLY!'
            }), 200

    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def settings_category(category_id):
    try:
        request_json = request.json
        if request.method == 'GET':
            products = Product.query.join(Category).filter_by(category_id=category_id).all()
            record = []
            for product in products:
                record.append({
                    'product_name': product.product_name,
                    'seller_name': product.category.category_name,
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
                'record': record,
            }), 200

        if request.method == 'DELETE':
            category = Category.query.get(category_id)
            db.session.delete(category)
            db.session.commit()
            return jsonify({
                'status': 200,
                'message': 'DELETE SUCCEED'
            }), 200

    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500
