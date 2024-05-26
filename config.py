from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask import Flask, request, jsonify, redirect



app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Config mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ichigovskirito@gmail.com'
app.config['MAIL_PASSWORD'] = 'eqol zanm zjgf nxit'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Connect to database
# Local host
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:dungnguyen2077@127.0.0.1:3306/devilmaycry'
app.config['SQLALCHEMY_BINDS'] = {
    'provide': 'mysql+mysqlconnector://root:dungnguyen2077@127.0.0.1:3306/vietnamese_administrative_units',
}
# Railway
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:NuHFMYkYalcNPYjebMtqLERYAORZCXry@monorail.proxy.rlwy.net:38821/railway'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = True

# Creating data base
db = SQLAlchemy(app)


@app.route("/send-mail", methods=['POST'])
def index():
    msg = Message('Hello', sender='ichigovskirito@gmail.com', recipients=['demokahootft@gmail.com'])
    html = f"""
                <!doctype html>
                <html>
                  <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                  </head>
                  <body style="font-family: sans-serif;">
                    <div style="display: block; margin: auto; max-width: 600px;" class="main">
                      <h1 style="font-size: 18px; font-weight: bold; margin-top: 20px">
                        Đơn hàng của bạn đã được đặt thành công!
                      </h1>
                      <p>Mã đơn hàng -  </p>
                        <table style="border-collapse: collapse;">
                            <tr>
                                <td style="border: 1px solid black; padding: 8px;">Cell 1</td>
                                <td style="border: 1px solid black; padding: 8px;">Cell 2</td>
                                <td style="border: 1px solid black; padding: 8px;">Cell 3</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid black; padding: 8px;">Cell 4</td>
                                <td style="border: 1px solid black; padding: 8px;">Cell 5</td>
                                <td style="border: 1px solid black; padding: 8px;">Cell 6</td>
                            </tr>
                        </table>
            
                      <p>Inspect it using the tabs you see above and learn how this email can be improved.</p>
                      
                      <p>Now send your email using our fake SMTP server and integration of your choice!</p>
                      <p style="color: red">Good luck! Hope it works.</p>
                    </div>

                  </body>
                </html>
                """

    msg.html = html
    mail.send(msg)
    return "Sent"
