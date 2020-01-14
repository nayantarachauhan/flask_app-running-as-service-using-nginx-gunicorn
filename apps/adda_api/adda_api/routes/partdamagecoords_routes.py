from adda_api.routes import *
from adda_api.views.partdamagecoords_api import PartDamageCoords

api.add_resource(PartDamageCoords,'/part_damage/coords')
