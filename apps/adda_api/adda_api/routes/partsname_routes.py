from adda_api.routes import *
from adda_api.views.partsname_api import PartsName_update, PartsName



api.add_resource(PartsName,'/parts_name')
api.add_resource(PartsName_update, '/parts_name/<int:id>/')
