from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Init app
app = Flask(__name__)

#Init DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:misiulek10@localhost:5432/MyAppDataBase'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from views import *

#Run server
if __name__ == '__main__':
    app.run(debug=True, port=105)