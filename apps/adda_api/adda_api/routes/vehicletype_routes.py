from adda_api.routes import *
from adda_api.views.vehicletype_api import VehicleType_update, VehicleType

api.add_resource(VehicleType_update, '/vehicle_type/<int:id>/')
api.add_resource(VehicleType,'/vehicle_type')
