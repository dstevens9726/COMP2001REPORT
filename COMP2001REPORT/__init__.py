import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://DStevens:EybZ719+@DIST-6-505.uopnet.plymouth.ac.uk/COMP2001_DStevens?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    try:
        db.engine.connect()
        print(app.url_map)
        print("Database Connected Successfully")
    except Exception as e:
        print("Error connecting to database:", e)

import models
import callProcedures  # Ensure that this contains the route definitions, but don't run the app here.

# Don't call app.run() here.

