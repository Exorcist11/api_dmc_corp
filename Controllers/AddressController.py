from Services.AddressServices import *
from config import app


app.add_url_rule('/address/<string:account_id>', methods=['GET', 'POST'], view_func=manage_address)
app.add_url_rule('/settings_address/<string:address_id>', methods=['DELETE', 'PATCH', 'GET'], view_func=setting_address)


