from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:NuHFMYkYalcNPYjebMtqLERYAORZCXry@monorail.proxy.rlwy.net:38821/railway'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = True

# Creating data base
db = SQLAlchemy(app)
