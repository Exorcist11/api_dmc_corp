from config import app
from Services.CartServices import *

app.add_url_rule('/add_to_cart', methods=['POST'], view_func=add_to_cart)
app.add_url_rule('/settings_cart/<string:account_id>', methods=['GET'], view_func=settings_cart)
app.add_url_rule('/remove_product', methods=['POST', 'PATCH'], view_func=remove_product_from_cart)

