from config import app
from Services.SellerServices import *


app.add_url_rule('/seller', methods=['POST', 'GET'], view_func=add_new_seller)
app.add_url_rule('/setting-seller/<string:seller_id>', methods=['GET', 'PATCH', 'DELETE'], view_func=manage_seller)
