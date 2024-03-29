from config import app
from Services.ProductServices import *


app.add_url_rule('/product', methods=['GET', 'POST'], view_func=manage_product)
app.add_url_rule('/product_by_seller/<string:seller_id>', methods=['GET'], view_func=get_product_by_seller)
