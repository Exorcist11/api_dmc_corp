import uuid
import bcrypt
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


def get_all_account():
    try:
        return True
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500
