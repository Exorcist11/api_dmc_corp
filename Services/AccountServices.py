import uuid
import bcrypt
from datetime import datetime
from flask import request, jsonify
from config import db
from Models.Accounts import Account
from Models.Users import User
from Models.Roles import Role


def register():
    try:
        request_form = request.json
        account_id = str(uuid.uuid4())
        username = request_form['username']
        if Account.query.filter_by(username=username).first() is not None:
            return jsonify({
                'status': 406,
                'message': 'Account already exists!'
            }), 406
        else:
            new_account = Account(
                account_id=account_id,
                username=username,
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


def login():
    try:
        request_form = request.json
        username = request_form['username']
        password = request_form['password']
        account = Account.query.filter_by(username=username).first()
        if account is None:
            return jsonify({
                'status': 404,
                'message': 'Username not found!'
            }), 404
        else:
            check_password = bcrypt.checkpw(password.encode('utf-8'), account.password.encode('utf-8'))
            if check_password:
                account.is_activated = True
                db.session.commit()
                record = {
                    'account_id': account.account_id,
                    'username': account.username
                }
                return jsonify({
                    'status': 200,
                    'message': 'Login successfully',
                    'info': record
                }), 200
            else:
                return jsonify({
                    'status': 401,
                    'message': 'Wrong password!'
                }), 401
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

            if not bcrypt.checkpw(old_password.encode('utf-8'), account.password.encode('utf-8')):
                return jsonify({
                    'status': 401,
                    'message': 'Wrong password!'
                }), 401
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


def logout(account_id):
    account = Account.query.filter_by(account_id=account_id).first()
    account.is_activated = False
    db.session.commit()
    return jsonify({
        'status': 200,
        'message': 'Logout successfully!'
    }), 200


def get_account_by_role():
    try:
        role_id = request.args.get('role_id')
        users = User.query.join(Account).join(Role).filter(Account.role_id == role_id).all()
        list_user = []

        for user in users:
            list_user.append({
                'full_name': user.full_name,
                'phone_number': user.phone_number,
                'email': user.email,
                'dob': user.date_of_birth,
                'time_register': user.time_register,
                'time_update': user.time_update,
                'is_deleted': user.is_deleted
            })

        if not users:
            return jsonify({
                'status': 404,
                'message': 'Users is null!'
            }), 404

        return jsonify({
            'status': 200,
            'list_user': list_user,
            'role': role_id
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def change_role(account_id):
    try:
        account = Account.query.filter_by(account_id=account_id).first_or_404()
        account.role_id = request.form.get('role')
        db.session.commit()

        return jsonify({
            'status': 200,
            'message': f'Change role successfully!'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500
