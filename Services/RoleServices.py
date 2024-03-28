from Models.Roles import Role
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


def delete_role(role_id):
    try:
        role = Role.query.filter_by(role_id=role_id).delete()
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': 'Success!'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500
