from flask import Flask, current_app, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session

from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.ext.automap import automap_base
from flask_admin import Admin
from flask import request,render_template, Response,redirect, url_for,jsonify
from flask_cors import CORS



db = SQLAlchemy()
jwt = JWTManager()
flask_bcrypt = Bcrypt()
admin = Admin()
Base = automap_base()
bootstrap = Bootstrap()
login_manager = LoginManager()
#sess = Session()

# from adda_admin.config import *

def create_app():
	# print("*****************************config_filename-----------", config_filename)
	app = Flask(__name__)
	CORS(app)
	app.config.from_object('config.Config')
	app.url_map.strict_slashes = False
	#app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

	@app.route('/')
	def index():
		return render_template('home.html')

	with app.app_context():

		from adda_admin.models.user import user

		db.init_app(app)
		Base.prepare(db.engine, reflect=True)
		
		flask_bcrypt = Bcrypt(app)
		bootstrap = Bootstrap(app)

		from adda_admin.views.adminview.customadminview import AdminIndex
		admin = Admin(app, base_template='my_master.html', index_view=AdminIndex(),template_mode = 'bootstrap3')
		
		jwt.init_app(app)
		login_manager.init_app(app)

		from adda_admin.routes import api_bp
		app.register_blueprint(api_bp, url_prefix='')

		from adda_admin.views.adminview import addAdminView,addContextProcessor
		addAdminView(admin)
		addContextProcessor(app)

		return app


