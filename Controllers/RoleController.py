from Services.RoleServices import *
from config import app


app.add_url_rule('/role', methods=['GET', 'POST'], view_func=manage_role)
app.add_url_rule('/role/<string:role_id>', methods=['DELETE'], view_func=delete_role)
