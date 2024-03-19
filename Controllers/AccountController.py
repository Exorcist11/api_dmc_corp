from config import app
from Services.AccountServices import *


app.add_url_rule('/register', methods=['GET', 'POST'], view_func=register)



