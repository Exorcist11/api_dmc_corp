from config import app
from Services.AccountServices import *


app.add_url_rule('/register', methods=['GET', 'POST'], view_func=register)
app.add_url_rule('/settings/<string:account_id>', methods=['GET', 'PATCH', 'PUT'], view_func=edit_account)



