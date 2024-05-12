from config import app
from Services.ReportServices import *


app.add_url_rule('/report_month/<int:year>', methods=['GET'], view_func=report_month)
app.add_url_rule('/report_month/<int:year>/<int:month>', methods=['GET'], view_func=report_days_in_month)
