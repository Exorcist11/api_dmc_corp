import uuid
import bcrypt
from datetime import datetime
from flask import request, jsonify
from config import db
from Models.Accounts import Account
from Models.Users import User


def register():
    try:
        request_form = request.form.to_dict()
        account_id = str(uuid.uuid4())
        new_account = Account(
            account_id=account_id,
            username=request_form['username'],
            password=bcrypt.hashpw(request_form['password'].encode('utf-8'), bcrypt.gensalt())
        )
        db.session.add(new_account)
        db.session.commit()

        new_user = User(
            account_id=account_id,
            full_name=str(uuid.uuid4())[:20]
        )
        db.session.add(new_user)
        db.session.commit()

        account = Account.query.get(account_id)

        return jsonify({
            'status': 200,
            'message': 'Register successfully!',
            'account_id': account.account_id
        }), 200

    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def edit_account(account_id):
    try:
        user = User.query.filter_by(account_id=account_id).first()
        request_form = request.form.to_dict()
        if user is None:
            return jsonify({
                'status': 404,
                'message': 'User not found!'
            }), 404
        if request.method == 'GET':
            infor = {
                'full_name': user.full_name,
                'phone_number': user.phone_number,
                'email': user.email,
                'date_of_birth': user.date_of_birth
            }
            return jsonify({
                'status': 200,
                'message': 'Success',
                'infor': infor
            }), 200
        elif request.method == 'PATCH':

            user.full_name = request_form['full_name']
            user.phone_number = request_form['phone_number']
            user.email = request_form['email']
            user.date_of_birth = request_form['dob']
            user.time_update = datetime.now()

            db.session.commit()
            response = User.query.filter_by(account_id=account_id).first()
            return jsonify({
                'status': 200,
                'message': 'Update user successfully!',
                'data': response.full_name
            }), 200
        elif request.method == 'PUT':
            account = Account.query.filter_by(account_id=account_id).first()
            if account is None:
                return jsonify({
                    'status': 404,
                    'message': 'Account not found!'
                }), 404
            old_password = request_form['password']
            if bcrypt.checkpw(old_password.encode('utf-8'), bcrypt.hashpw(account.password.encode('utf-8'), bcrypt.gensalt())) == False:
                return jsonify({
                    'status': 301,
                    'message': 'Wrong password!'
                }), 301
            else:
                account.password = bcrypt.hashpw(request_form['new_password'].encode('utf-8'), bcrypt.gensalt())
                db.session.commit()
                return jsonify({
                    'status': 200,
                    'message': 'Change password successfully!'
                }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500
