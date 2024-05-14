from config import app
from Services.OrderServices import *


app.add_url_rule('/checkout_cart', methods=['POST'], view_func=cart_checkout)
app.add_url_rule('/action_order', methods=['POST'], view_func=active_order)
app.add_url_rule('/get_order', methods=['GET'], view_func=get_order)
app.add_url_rule('/get_order_pending', methods=['GET'], view_func=get_order_pending)
app.add_url_rule('/get_order/<string:order_id>', methods=['GET'], view_func=get_order_detail)
app.add_url_rule('/get_order_pending', methods=['GET'], view_func=get_order_pending)
app.add_url_rule('/get_order_by_status/<string:status>', methods=['GET'], view_func=get_order_by_action)
app.add_url_rule('/get_order_by_customer/<string:account_id>', methods=['GET'], view_func=get_order_by_account)
app.add_url_rule('/review_product', methods=['POST'], view_func=review_by_customer)
app.add_url_rule('/get_review/<string:product_id>', methods=['GET'], view_func=get_review)
app.add_url_rule('/get_product_bought/<string:account_id>', methods=['GET'], view_func=get_product_by_user_bought)
app.add_url_rule('/detail_review/<string:order_id>/<string:product_id>', methods=['GET'], view_func=get_review_product)
