from config import db
import uuid
import bcrypt
from datetime import datetime
from flask import request, jsonify
from Models.Accounts import Account
from Models.Orders import *
from Models.Products import *
from Models.Images import *
from Models.Users import User
from Models.Roles import Role
from Models.Address import Address
from Services.Middleware import *
from Models.Provides import *
from sqlalchemy import func


def register():
    try:
        request_form = request.json
        account_id = generate_custom_id('USER')
        username = request_form['username']
        if Account.query.filter_by(username=username).first() is not None:
            return jsonify({
                'status': 409,
                'message': 'Account already exists!'
            }), 409
        else:
            password = request_form['password']
            if len(password) < 8:
                return jsonify({
                    'status': 422,
                    'message': 'Invalid length'
                }), 422
            else:
                new_account = Account(
                    account_id=account_id,
                    username=username,
                    password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
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
        db.session.rollback()
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
                    'username': account.username,
                    'role_id': account.role_id
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

        if user is None:
            return jsonify({
                'status': 404,
                'message': 'User not found!'
            }), 404
        if request.method == 'GET':
            address = Address.query.filter_by(account_id=user.account_id).all()
            record = []
            for item in address:
                province = Province.query.filter_by(code=item.province).first()
                district = District.query.filter_by(code=item.district).first_or_404()
                ward = Ward.query.filter_by(code=item.ward).first()
                record.append({
                    'address_id': item.address_id,
                    'full_name': item.full_name,
                    'phone_number': item.phone_number,
                    'province': province.full_name,
                    'district': district.full_name,
                    'ward': ward.full_name,
                    'note': item.note
                })

            infor = {
                'user_id': user.account_id,
                'user_name': user.account.username,
                'full_name': user.full_name,
                'phone_number': user.phone_number,
                'email': user.email,
                'date_of_birth': user.date_of_birth,
                'address': record
            }
            return jsonify({
                'status': 200,
                'message': 'Success',
                'infor': infor
            }), 200
        elif request.method == 'PATCH':
            request_json = request.json
            user.full_name = request_json.get('full_name')
            user.phone_number = request_json['phone_number']
            user.email = request_json['email']
            user.date_of_birth = request_json.get('dob')
            user.time_update = datetime.now()

            db.session.commit()
            response = User.query.filter_by(account_id=account_id).first()
            return jsonify({
                'status': 200,
                'message': 'Update user successfully!',
                'data': response.full_name
            }), 200
        elif request.method == 'PUT':
            request_json = request.json
            account = Account.query.filter_by(account_id=account_id).first()
            if account is None:
                return jsonify({
                    'status': 404,
                    'message': 'Account not found!'
                }), 404
            old_password = request_json['password']

            if not bcrypt.checkpw(old_password.encode('utf-8'), account.password.encode('utf-8')):
                return jsonify({
                    'status': 401,
                    'message': 'Wrong password!'
                }), 401
            else:
                account.password = bcrypt.hashpw(request_json['new_password'].encode('utf-8'), bcrypt.gensalt())
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


def get_all_account():
    try:
        users = User.query.join(Account).join(Role).all()
        list_user = []

        for user in users:
            list_user.append({
                'account_id': user.account_id,
                'username': user.account.username,
                'full_name': user.full_name,
                'phone_number': user.phone_number,
                'email': user.email,
                'dob': user.date_of_birth,
                'time_register': user.time_register,
                'time_update': user.time_update,
                'is_deleted': user.is_deleted,
                'role': user.account.role.role_id
            })

        if not users:
            return jsonify({
                'status': 404,
                'message': 'Users is null!'
            }), 404

        return jsonify({
            'status': 200,
            'list_user': list_user,
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


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


def dashboard():
    try:
        account = db.session.query(Account).count()
        product_quantity = db.session.query(Product).count()
        total_completed_orders = db.session.query(
            func.sum(Order.total).label('total_x')
        ).filter(
            Order.status == 'completed'
        ).first()

        products = Product.query.order_by(Product.create_at.desc()).limit(5).all()
        record = []
        for product in products:
            images = Image.query.filter_by(product_id=product.product_id).all()
            image_url = [image.url for image in images]
            record.append({
                'product_id': product.product_id,
                'product_name': product.product_name,
                'seller_name': product.seller.seller_name,
                'nation': product.seller.nation,
                'price': product.price,
                'amount': product.amount,
                'category': product.category.category_name,
                'rate': product.rate,
                'color': product.color,
                'material': product.material,
                'size': product.size,
                'width': product.width,
                'waterproof': product.waterproof,
                'description_display': product.description_display,
                'description_markdown': product.description_markdown,
                'images': image_url,
                'path_product': product.path_product
            })

        accounts = Account.query.all()
        new_acc = []
        for ac in accounts:
            new_acc.append({
                'account_id': ac.account_id,
                'create_at': ac.time_register,
                'username': ac.username
            })

        return jsonify({
            'new_product': record,
            'account': account,
            'product': product_quantity,
            'summary': total_completed_orders.total_x,
            'new_account': new_acc
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500
