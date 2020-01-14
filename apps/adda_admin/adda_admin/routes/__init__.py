
from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from adda_admin.routes.user_registerNlogin_routes import *














