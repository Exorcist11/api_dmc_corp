from Services.AddressServices import *
from config import app


app.add_url_rule('/address/<string:account_id>', methods=['GET', 'POST'], view_func=manage_address)
app.add_url_rule('/settings_address/<string:address_id>', methods=['DELETE', 'PATCH', 'GET'], view_func=setting_address)
app.add_url_rule('/provinces', methods=['GET'], view_func=get_all_provinces)
app.add_url_rule('/provinces/<string:province_id>', methods=['GET'], view_func=get_district_by_province)
app.add_url_rule('/provinces/<string:province_id>/<string:district_id>', methods=['GET'], view_func=get_ward_by_district)
