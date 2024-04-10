from flask import jsonify, request
from Models.Sellers import Seller
from config import db
from datetime import datetime
from Services.Middleware import *


def add_new_seller():
    try:
        if request.method == 'POST':
            request_form = request.json
            new_seller = Seller(
                seller_name=request_form['seller_name'],
                description=request_form.get('description', None),
                nation=request_form['nation'],
                path_seller=convert_to_ascii(request_form['seller_name'])
            )
            db.session.add(new_seller)
            db.session.commit()

            return jsonify({
                'status': 200,
                'message': 'Add new seller successfully!'
            }), 200

        if request.method == 'GET':
            sellers = Seller.query.all()
            data = []
            for seller in sellers:
                info = {
                    'seller_id': seller.seller_id,
                    'seller_name': seller.seller_name,
                    'description': seller.description,
                    'nation': seller.nation,
                    'create_at': seller.create_at,
                    'update_at': seller.update_at,
                    'is_activated': seller.is_activated
                }
                data.append(info)

            if data is None:
                return jsonify({
                    'status': 200,
                    'message': 'List sellers empty',
                }), 200

            return jsonify({
                'status': 200,
                'message': 'List sellers',
                'data': data
            }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def manage_seller(seller_id):
    try:
        request_form = request.form.to_dict()
        seller = Seller.query.filter_by(seller_id=seller_id).first()
        if seller is None:
            return jsonify({
                'status': 404,
                'message': 'Seller not found!'
            }), 404
        if request.method == 'GET':
            data = {
                'seller_id': seller.seller_id,
                'seller_name': seller.seller_name,
                'description': seller.description,
                'nation': seller.nation,
                'create_at': seller.create_at,
                'update_at': seller.update_at,
                'is_activated': seller.is_activated
            }

            return jsonify({
                'status': 200,
                'message': f'Seller {seller.seller_id}',
                'data': data
            }), 200

        if request.method == 'PATCH':
            seller.seller_name = request_form['seller_name'],
            seller.description = request_form['description'],
            seller.nation = request_form['nation'],
            seller.update_at = datetime.now(),
            seller.is_activated = True if request_form['active'] == str('1') else False
            db.session.commit()

            data_update = {
                'seller_id': seller.seller_id,
                'seller_name': seller.seller_name,
                'description': seller.description,
                'nation': seller.nation,
                'create_at': seller.create_at,
                'update_at': seller.update_at,
                'is_activated': seller.is_activated
            }
            return jsonify({
                'status': 200,
                'message': f'Update seller {seller_id} successfully!',
                'data': data_update
            }), 200

        if request.method == 'DELETE':
            Seller.query.filter_by(seller_id=seller_id).delete()
            db.session.commit()
            return jsonify({
                'status': 200,
                'message': 'Delete seller successfully'
            }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


