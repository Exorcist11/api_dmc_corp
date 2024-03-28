from Models.Users import User
from Models.Address import Address
from config import db
from flask import jsonify, request
from datetime import datetime


def manage_address(account_id):
    try:
        request_form = request.json

        if request.method == 'POST':
            new_address = Address(
                account_id=account_id,
                full_name=request_form['full_name'],
                phone_number=request_form['phone_number'],
                province=request_form['province'],
                district=request_form['district'],
                ward=request_form['ward'],
            )
            db.session.add(new_address)
            db.session.commit()
            addresses = Address.query.join(User.address).filter_by(account_id=account_id).all()
            list_address = []

            for address in addresses:
                list_address.append({
                    'address_id': address.address_id,
                    'full_name': address.full_name,
                    'phone_number': address.phone_number,
                    'province': address.province,
                    'district': address.district,
                    'ward': address.ward
                })

            return jsonify({
                'status': 200,
                'data': list_address,
                'user_name': addresses.full_name
            }), 200

        if request.method == 'GET':
            list_address = []
            for address in Address.query.join(User.address).filter_by(account_id=account_id).all():
                list_address.append({
                    'address_id': address.address_id,
                    'full_name': address.full_name,
                    'phone_number': address.phone_number,
                    'province': address.province,
                    'district': address.district,
                    'ward': address.ward
                })

            return jsonify({
                'status': 200,
                'list_address': list_address
            }), 200

    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def setting_address(address_id):
    try:
        address = Address.query.filter_by(address_id=address_id).first_or_404()
        request_form = request.form.to_dict()

        if request.method == 'PATCH':
            address.full_name = request_form['full_name']
            address.phone_number = request_form['phone_number']
            address.province = request_form['province']
            address.ward = request_form['ward']
            address.update_at = datetime.now()
            db.session.commit()

            after = Address.query.filter_by(address_id=address_id).first_or_404()
            data = {
                'address_id': after.address_id,
                'full_name': after.full_name,
                'phone_number': after.phone_number,
                'province': after.province,
                'district': after.district,
                'ward': after.ward,
                'update_at': after.update_at
            }

            return jsonify({
                'status': 200,
                'address_update': data,
                'message': 'Update address successfully!'
            }), 200

        if request.method == 'DELETE':
            Address.query.filter_by(address_id=address_id).delete()
            db.session.commit()
            return jsonify({
                'status': 200,
                'message': 'Delete address successfully!'
            }), 200

        if request.method == 'GET':
            data = {
                'address_id': address.address_id,
                'full_name': address.full_name,
                'phone_number': address.phone_number,
                'province': address.province,
                'district': address.district,
                'ward': address.ward,
                'update_at': address.update_at,
                'create_at': address.update_at
            }
            return jsonify({
                'status': 200,
                'data': data
            }), 200

    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500
