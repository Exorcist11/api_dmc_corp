from config import app
from Services.AccountServices import *

app.add_url_rule('/register', methods=['GET', 'POST'], view_func=register)
app.add_url_rule('/login', methods=['POST'], view_func=login)
app.add_url_rule('/logout/<string:account_id>', methods=['POST'], view_func=logout)
app.add_url_rule('/settings/<string:account_id>', methods=['GET', 'PATCH', 'PUT'], view_func=edit_account)
app.add_url_rule('/list_account', methods=['GET'], view_func=get_account_by_role)
app.add_url_rule('/get-all-account', methods=['GET'], view_func=get_all_account)
app.add_url_rule('/change_role/<string:account_id>', methods=['PATCH'], view_func=change_role)
app.add_url_rule('/dashboard', methods=['GET'], view_func=dashboard)
