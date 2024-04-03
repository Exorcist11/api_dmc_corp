from flask import Flask
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

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
