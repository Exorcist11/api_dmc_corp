from Models.Users import User
from Models.Address import Address
from config import db
from flask import jsonify, request
from datetime import datetime
from Models.Provides import *
from sqlalchemy import desc


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
                note=request_form['note'],
                is_activated=0
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
            lst_address = Address.query.join(User.address).filter_by(account_id=account_id).order_by(desc(Address.is_activated)).limit(3).all()
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

        if request.method == 'PATCH':
            request_form = request.json
            address.full_name = request_form['full_name'],
            address.phone_number = request_form['phone_number'],
            address.province = request_form['province'],
            address.district = request_form['district'],
            address.ward = request_form['ward'],
            address.note = request_form['note']
            address.update_at = datetime.now()
            db.session.commit()

            after = Address.query.filter_by(address_id=address_id).first_or_404()
            province = Province.query.filter_by(code=after.province).first()
            district = District.query.filter_by(code=after.district).first()
            ward = Ward.query.filter_by(code=after.ward).first()
            data = {
                'address_id': after.address_id,
                'full_name': after.full_name,
                'phone_number': after.phone_number,
                'province': province.name if province else None,
                'district': district.name if district else None,
                'ward': ward.name if ward else None,
                'note': after.note
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
            province = Province.query.filter_by(code=address.province).first()
            district = District.query.filter_by(code=address.district).first()
            ward = Ward.query.filter_by(code=address.ward).first()
            data = {
                'address_id': address.address_id,
                'full_name': address.full_name,
                'phone_number': address.phone_number,
                'province': province.name if province else None,
                'district': district.name if district else None,
                'ward': ward.name if ward else None,
                'note': address.note
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


def set_active_address():
    try:
        request_json = request.json
        address_id = request_json.get('address_id')

        address = Address.query.filter_by(address_id=address_id).first()

        if not address:
            return jsonify({
                'status': 404,
                'message': 'Address not found'
            }), 404

        address.is_activated = True

        other_addresses = Address.query.filter(Address.address_id != address_id).all()
        for other_address in other_addresses:
            other_address.is_activated = False

        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Default address updated successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_default_address(account_id):
    try:
        address = Address.query.join(User.address).filter_by(account_id=account_id, is_activated=1).order_by(
            desc(Address.update_at)).first()
        list_address = []
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


def get_ward_by_district(district_id):
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
