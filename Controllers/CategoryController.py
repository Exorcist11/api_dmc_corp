from Services.CategoryServices import *
from config import app


app.add_url_rule('/categories', methods=['GET', 'POST'], view_func=manage_category)
app.add_url_rule('/settings_category/<string:category_id>', methods=['GET', 'PATCH', 'DELETE'], view_func=settings_category)
