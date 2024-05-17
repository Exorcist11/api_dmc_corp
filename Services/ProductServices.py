from Models import OrderProduct
from Models.Products import Product
from Models.Images import Image
from Models.Categories import Category
from Models.WishList import WishList
from Services.Middleware import *
from flask import request, jsonify, send_from_directory
from sqlalchemy import desc, func
from config import db
from werkzeug.utils import secure_filename
import os


def manage_product():
    try:
        if request.method == 'POST':
            request_form = request.json
            new_product = Product(
                product_id=request_form['product_id'],
                product_name=request_form['product_name'],
                path_product=convert_to_ascii(request_form['product_name']),
                seller_id=request_form['seller'],
                category_id=request_form['category_id'],
                price=request_form.get('price', None),
                amount=request_form.get('amount', None),
                color=request_form.get("color", None),
                material=request_form.get('material', None),
                size=request_form.get('size', None),
                width=request_form.get('width', None),
                waterproof=request_form.get('waterproof', None),
                description_display=request_form.get('description_display', None),
                description_markdown=request_form.get('description_markdown', None)
            )
            db.session.add(new_product)
            db.session.commit()

            return jsonify({
                'status': 200,
                'message': 'ADD SUCCESSFULLY'
            })

        if request.method == 'GET':
            products = Product.query.order_by(desc(Product.create_at)).all()
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
                    'category': product.category.category_name ,
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
            return jsonify({
                'status': 200,
                'record': record
            }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def setting_product(product_id):
    try:
        product = Product.query.filter_by(product_id=product_id).first_or_404()
        images = Image.query.filter_by(product_id=product.product_id).all()
        image_url = [image.url for image in images]
        if request.method == 'GET':
            info_product = {
                'product_id': product.product_id,
                'product_name': product.product_name,
                'seller_name': product.seller.seller_name,
                'nation': product.seller.nation,
                'price': product.price,
                'amount': product.amount,
                'rate': product.rate,
                'color': product.color,
                'material': product.material,
                'size': product.size,
                'width': product.width,
                'waterproof': product.waterproof,
                'description_markdown': product.description_markdown,
                'description_html': product.description_display,
                'images': image_url if image_url else None,
            }
            return jsonify({
                'status': 200,
                'product': info_product,
                'message': 'INFOR PRODUCT'
            })
        if request.method == 'PATCH':
            request_json = request.json
            product.product_id = request_json['product_id'],
            product.product_name = request_json['product_name'],
            product.seller_id = request_json['seller'],
            product.category_id = request_json['category_id'],
            product.price = request_json.get('price', None),
            product.amount = request_json.get('amount', None),
            product.color = request_json.get("color", None),
            product.material = request_json.get('material', None),
            product.size = request_json.get('size', None),
            product.width = request_json.get('width', None),
            product.waterproof = request_json.get('waterproof', None),
            product.description = request_json.get('description', None)

            after = Product.query.filter_by(product_id=product_id).first_or_404()
            info_product = {
                'product_name': after.product_name,
                'seller_name': after.seller.seller_name,
                'nation': after.seller.nation,
                'price': after.price,
                'amount': after.amount,
                'rate': after.rate,
                'color': after.color,
                'material': after.material,
                'size': after.size,
                'width': after.width,
                'waterproof': after.waterproof,
                'description': after.description
            }
            return jsonify({
                'satus': 200,
                'message': 'SUCCESS',
                'product': info_product
            }), 200

        if request.method == 'DELETE':
            db.session.delete(product)
            db.session.commit()

            return jsonify({
                'satus': 200,
                'message': 'DELETE SUCCESS',
            }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_image(filename):
    return send_from_directory('Images', filename)


def get_product_by_seller(seller_id):
    try:
        if request.method == 'GET':
            products = Product.query.filter_by(seller_id=seller_id).all()
            list_product = []
            for product in products:
                list_product.append({
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'seller_name': product.seller.seller_name,
                    'nation': product.seller.nation,
                    'price': product.price,
                    'amount': product.amount,
                    'rate': product.rate,
                    'color': product.color,
                    'material': product.material,
                    'size': product.size,
                    'width': product.width,
                    'waterproof': product.waterproof,
                    'description': product.description
                })
            return jsonify({
                'status': 200,
                'list_product': list_product
            }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def upload_images():
    if 'images' not in request.files:
        return 'No images part', 400
    images = request.files.getlist('images')
    request_form = request.form

    image_folder = 'Images'

    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    for image in images:
        filename = secure_filename(image.filename)
        mimetype = image.mimetype
        if not filename or not mimetype:
            continue

        image_path = os.path.join(image_folder, filename)
        image.save(image_path)
        new_image = Image(
            url=f'{request.host_url}images/{filename}',
            content_type=mimetype,
            product_id=request_form.get('product_id', ''),
            account_id=request_form.get('user_id', '')
        )
        db.session.add(new_image)
    db.session.commit()
    return 'Images have been uploaded successfully', 200


def get_product_by_category(path_category):
    try:
        products = Product.query.join(Category).filter(Category.path_category == path_category).order_by(Product.create_at.desc()).all()
        category = Category.query.filter_by(path_category=path_category).first()

        record = []
        for product in products:
            images = Image.query.filter_by(product_id=product.product_id).all()
            image_url = [image.url for image in images]
            record.append({
                'product_id': product.product_id,
                'product_name': product.product_name,
                'seller_name': product.seller.seller_name,
                'nation': product.seller.nation,
                'category': product.category.category_name,
                'price': product.price,
                'amount': product.amount,
                'rate': product.rate,
                'color': product.color,
                'material': product.material,
                'size': product.size,
                'width': product.width,
                'waterproof': product.waterproof,
                'description_display': product.description_display,
                'description_markdown': product.description_markdown,
                'images': image_url[0] if image_url else None,
                'path_product': product.path_product
            })
        return jsonify({
            'record': record,
            'status': 200,
            'category': category.category_name
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_product_by_path_product(path_product):
    try:
        product = Product.query.filter_by(path_product=path_product).first_or_404()
        images = Image.query.filter_by(product_id=product.product_id).all()
        image_url = [image.url for image in images]
        record = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'seller_name': product.seller.seller_name,
            'nation': product.seller.nation,
            'price': product.price,
            'amount': product.amount,
            'category': product.category.category_name,
            'path_category': product.category.path_category,
            'rate': product.rate,
            'color': product.color,
            'material': product.material.capitalize(),
            'size': product.size,
            'width': product.width,
            'waterproof': product.waterproof,
            'description_display': product.description_display,
            'description_markdown': product.description_markdown,
            'images': image_url if image_url else None,
            'path_product': product.path_product
        }
        return jsonify({
            'status': 200,
            'record': record
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_best_product():
    try:
        best_sellers = db.session.query(
            Product.product_id,
            Product.product_name,
            Product.price,
            Product.path_product,
            func.sum(OrderProduct.amount).label('total_sold')
        ).join(
            OrderProduct, Product.product_id == OrderProduct.product_id
        ).group_by(
            Product.product_id
        ).order_by(
            func.sum(OrderProduct.amount).desc()
        ).limit(8).all()

        best_sellers_json = []
        for product in best_sellers:
            images = Image.query.filter_by(product_id=product.product_id).all()
            image = [image.url for image in images]
            product_data = {
                'product_id': product.product_id,
                'product_name': product.product_name,
                'price': product.price,
                'path': product.path_product,
                'images': image[0],
                'total_sold': product.total_sold,

            }
            best_sellers_json.append(product_data)

        return jsonify({
            'record': best_sellers_json,
            'category': 'Best seller'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def add_to_wishlist():
    try:
        request_json = request.json
        account_id = request_json.get('account_id')
        product_id = request_json.get('product_id')
        if not account_id or not product_id:
            return jsonify({
                'status': 400,
                'message': 'Missing required fields!'
            }), 400

        product = Product.query.filter_by(product_id=product_id).first()

        if product is None:
            return jsonify({
                'status': 404,
                'message': 'Product not found!'
            }), 404

        favorite = WishList.query.filter_by(account_id=account_id, product_id=product_id).first()
        if favorite is None:
            wish_list = WishList(
                account_id=account_id,
                product_id=product_id
            )
            db.session.add(wish_list)
            db.session.commit()
            return jsonify({
                'status': 200,
                'message': 'Add product to wishlist success!'
            }), 200
        else:
            return jsonify({
                'status': 400,
                'message': 'Product already exists in wishlist!'
            }), 400

    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def remove_wish_list():
    try:
        request_json = request.json
        account_id = request_json.get('account_id')
        product_id = request_json.get('product_id')
        wish_list = WishList.query.filter_by(account_id=account_id, product_id=product_id).first()
        if wish_list is None:
            return jsonify({
                'status': 404,
                'message': 'Product not found!'
            }), 404
        db.session.delete(wish_list)
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': 'Delete product from wishlist'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def get_wish_list(user_id):
    try:
        wish = WishList.query.filter_by(account_id=user_id).all()
        record = []
        for item in wish:
            product = Product.query.filter_by(product_id=item.product_id).first()
            images = Image.query.filter_by(product_id=item.product_id).all()
            image = [image.url for image in images]
            record.append({
                'image': image[0],
                'product_name': product.product_name,
                'path_product': product.path_product,
                'price': product.price
            })
        return jsonify({
            'status': 200,
            'record': record
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def favorite_product_account():
    try:
        request_json = request.json
        account_id = request_json.get('account_id')
        product_id = request_json.get('product_id')
        favorite = WishList.query.filter_by(account_id=account_id, product_id=product_id).first()
        if favorite is None:
            return jsonify({
                'status': 200,
                'action': False
            }), 200
        else:
            return jsonify({
                'status': 200,
                'action': True
            }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def search_product_by_name():
    try:
        request_json = request.json
        name = request_json.get('name')
        products = Product.query.filter(Product.product_name.ilike(f'%{name}%')).all()
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
        return jsonify({
            'status': 200,
            'record': record
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def category_product(path):
    try:
        if path == 'dong-ho':
            products = Product.query.join(Category).filter(Category.path_category == 'dong-ho').all()
        else:
            products = Product.query.join(Category).filter(Category.path_category != 'dong-ho').all()

        record = []
        for product in products:
            images = Image.query.filter_by(product_id=product.product_id).all()
            image_url = [image.url for image in images]
            record.append({
                'product_id': product.product_id,
                'product_name': product.product_name,
                'seller_name': product.seller.seller_name,
                'nation': product.seller.nation,
                'category': product.category.category_name,
                'price': product.price,
                'amount': product.amount,
                'rate': product.rate,
                'color': product.color,
                'material': product.material,
                'size': product.size,
                'width': product.width,
                'waterproof': product.waterproof,
                'description_display': product.description_display,
                'description_markdown': product.description_markdown,
                'images': image_url[0] if image_url else None,
                'path_product': product.path_product
            })
        return jsonify({
            'record': record,
            'status': 200
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def search_param():
    try:
        args = request.args
        value = args.get('value')
        products = Product.query.filter(Product.product_name.ilike(f'%{value}%')).all()
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
        return jsonify({
            'status': 200,
            'record': record
        }), 200
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500
