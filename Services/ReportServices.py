from config import *
from flask import request, jsonify
from sqlalchemy import func
from datetime import datetime, timedelta
from Models.Orders import *


def report_month(year):
    try:
        reports = []
        for month in range(1, 13):
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month % 12 + 1, 1) if month < 12 else datetime(year + 1, 1, 1)

            completed_orders = db.session.query(OrderProduct, Order)\
                .join(Order, OrderProduct.order_id == Order.order_id)\
                .filter(
                    Order.status == 'completed',
                    Order.update_at >= start_date,
                    Order.update_at < end_date
                ).all()

            total_revenue = 0
            for order_product in completed_orders:
                total_revenue += order_product.OrderProduct.amount * order_product.OrderProduct.price
            report = {
                'year': year,
                'month': f'Tháng {month}',
                'total_revenue': total_revenue,
                'orders': []
            }

            for order in completed_orders:
                order_info = {
                    'order_id': order.Order.order_id,
                    'total': order.Order.total,
                    'products': []
                }
                for product in order.Order.products:
                    order_info['products'].append({
                        'name': product.product_name,
                        'quantity': product.amount,
                        'price': product.price
                    })
                report['orders'].append(order_info)

            report['total_revenue'] = total_revenue
            reports.append(report)

        return jsonify(reports)
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500


def report_days_in_month(year, month):
    try:
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month % 12 + 1, 1) if month < 12 else datetime(year + 1, 1, 1)

        daily_sales = []
        current_date = start_date
        while current_date < end_date:
            next_date = current_date + timedelta(days=1)

            completed_orders = db.session.query(OrderProduct). \
                join(Order, OrderProduct.order_id == Order.order_id). \
                filter(Order.status == 'completed',
                       Order.update_at >= current_date,
                       Order.update_at < next_date).all()

            total_sales = 0
            for order_product in completed_orders:
                total_sales += order_product.amount * order_product.price

            daily_sales.append({
                'date': current_date.strftime('%d-%m-%Y'),
                'total_sales': total_sales
            })

            current_date = next_date

        return jsonify({
            'year': year,
            'month': month,
            'daily_sales': daily_sales
        })
    except Exception as e:
        return jsonify({
            'status': 500,
            'message': f'Error: {e}'
        }), 500

