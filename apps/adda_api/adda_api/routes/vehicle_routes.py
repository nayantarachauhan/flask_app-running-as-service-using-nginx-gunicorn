from adda_api.routes import *
from adda_api.views.vehicle_api import Vehicle, Vehicle_update


api.add_resource(Vehicle, '/vehicle')
api.add_resource(Vehicle_update, '/vehicle/<int:vehicle_id>/')