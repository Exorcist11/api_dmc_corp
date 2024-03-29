from Models.Roles import Role
from Models.Accounts import Account
from Models.Users import User
from flask import request, jsonify
from config import db


def manage_role():
    try:
        if request.method == 'GET':
            roles = Role.query.all()
            list_role = []
            for role in roles:
                list_role.append({
                    'role_id': role.role_id,
                    'role_name': role.role_name
                })

            if list_role is None:
                return jsonify({
                    'status': 404,
                    'message': 'List role is empty'
                }), 404
            return jsonify({
                'status': 200,
                'list_role': list_role,
            }), 200

        if request.method == 'POST':
            request_json = request.json
            new_role = Role(
                role_id=request_json['role_id'],
                role_name=request_json.get('role_name', None)
            )
            db.session.add(new_role)
            db.session.commit()

            return jsonify({
                'status': 200,
                'role_id': request_json['role_id']
            }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def all_delete_role(role_id):
    try:
        if request.method == 'DELETE':
            role = Role.query.filter_by(role_id=role_id).delete()
            db.session.commit()
            return jsonify({
                'status': 200,
                'message': 'Success!'
            }), 200
        if request.method == 'GET':
            # role_by_id = User.query.join(Account).join(Role).add_column(Account.username).filter_by(role_id=role_id).all()
            list_user_by_id = []
            users = User.query.join(Account).filter_by(role_id=role_id).all()

            for user in users:
                list_user_by_id.append({
                    'user_id': user.account_id,
                    'username': user.account.username,
                    'full_name': user.full_name,
                    'phone_number': user.phone_number,
                    'email': user.email,
                    'date_of_birth': user.date_of_birth,
                    'create_at': user.time_register,
                    'update_at': user.time_update
                })
            return jsonify({
                'status': 200,
                'message': f'List user by Role {role_id}',
                'users': list_user_by_id
            }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500
