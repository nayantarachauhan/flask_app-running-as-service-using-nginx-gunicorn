
from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


from adda_api.routes.master_config_routes import *
from adda_api.routes.user_registerNlogin_routes import *
from adda_api.routes.incs_config_routes import *
from adda_api.routes.external_config_routes import *
from adda_api.routes.client_config_routes import *
from adda_api.routes.accesslevel_config_routes import *
from adda_api.routes.partsname_routes import *
from adda_api.routes.vehicletype_routes import *
from adda_api.routes.partdamagecoords_routes import *
from adda_api.routes.damagecoords_routes import *
from adda_api.routes.assessreport_routes import *
from adda_api.routes.assessment_routes import *
from adda_api.routes.vehicle_routes import *
from adda_api.routes.carimage_routes import *
from adda_api.routes.damage_routes import *
from adda_api.routes.partdamage_routes import *
from adda_api.routes.part_routes import *
from adda_api.routes.uploads_routes import *













