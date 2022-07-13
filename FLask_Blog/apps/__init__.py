from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "geekscoderssecretkey"
<<<<<<< HEAD
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Ismilelabn209!!@172.23.142.168:3306/db_ismile' # Connect to Database Server
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:MilitenSire360@localhost:3306/db_ismile' # Connect to Database Server
=======
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Ismilelabn209!!@172.23.142.168:3306/db_ismile' # Connect to Database Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:root@localhost:3306/i-smile' # Connect to Database Server
>>>>>>> 6e9fd3ac68b230973c56cc83568f31740eb5ac40
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from apps import routes