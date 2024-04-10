from config import app
from Services.ProductServices import *


app.add_url_rule('/product', methods=['GET', 'POST'], view_func=manage_product)
app.add_url_rule('/settings_product/<string:product_id>', methods=['GET', 'PATCH', 'DELETE'],  view_func=setting_product)
app.add_url_rule('/product_by_seller/<string:seller_id>', methods=['GET'], view_func=get_product_by_seller)
app.add_url_rule('/product/best-seller', methods=['GET'], view_func=get_best_product)
app.add_url_rule('/upload-images', methods=['POST'], view_func=upload_images)
app.add_url_rule('/images/<filename>', methods=['GET'], view_func=get_image)
app.add_url_rule('/product_by_category/<string:path_category>', methods=['GET'], view_func=get_product_by_category)
app.add_url_rule('/product_by_path/<string:path_product>', methods=['GET'], view_func=get_product_by_path_product)

