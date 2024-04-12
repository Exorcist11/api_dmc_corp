from config import app
from Services.CartServices import *

app.add_url_rule('/add_to_cart', methods=['POST'], view_func=add_to_cart)

