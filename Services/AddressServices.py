from Models.Users import User
from Models.Address import Address
from config import db
from flask import jsonify, request
from datetime import datetime
from Models.Provides import *


def manage_address(account_id):
    try:
        if request.method == 'POST':
            request_form = request.json
            new_address = Address(
                account_id=account_id,
                full_name=request_form['full_name'],
                phone_number=request_form['phone_number'],
                province=request_form['province'],
                district=request_form['district'],
                ward=request_form['ward'],
                note=request_form['note']
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
                'data': list_address
            }), 200

        if request.method == 'GET':
            lst_address = Address.query.join(User.address).filter_by(account_id=account_id).limit(3).all()
            list_address = []
            for address in lst_address:
                province = Province.query.filter_by(code=address.province).first()
                district = District.query.filter_by(code=address.district).first()
                ward = Ward.query.filter_by(code=address.ward).first()
                list_address.append({
                    'address_id': address.address_id,
                    'full_name': address.full_name,
                    'phone_number': address.phone_number,
                    'province': province.name if province else None,
                    'district': district.name if district else None,
                    'ward': ward.name if ward else None,
                    'note': address.note
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


def get_all_provinces():
    try:
        provinces = Province.query.all()
        record = []
        for province in provinces:
            record.append({
                'code': province.code,
                'name': province.name,
                'full_name': province.full_name,
                'code_name': province.code_name
            })
        return jsonify({
            'status': 200,
            'provinces': record
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_district_by_province(province_id):
    try:
        districts = District.query.filter_by(province_code=province_id).all()
        province = Province.query.filter_by(code=province_id).first_or_404()
        record = []
        for district in districts:
            record.append({
                'code': district.code,
                'name': district.name,
                'full_name': district.full_name,
                'code_name': district.code_name
            })
        return jsonify({
            'status': 200,
            'province': province.name,
            'districts': record
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_ward_by_district(province_id, district_id):
    try:
        district = District.query.filter_by(code=district_id).first_or_404()
        wards = Ward.query.filter_by(district_code=district_id).all()
        record = []
        for ward in wards:
            record.append({
                'code': ward.code,
                'name': ward.name,
                'full_name': ward.full_name,
                'code_name': ward.code_name
            })
        return jsonify({
            'status': 200,
            'district': district.name,
            'ward': record
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500