from adda_api.routes import *
from adda_api.views.damagecoords_api import DamageCoords


api.add_resource(DamageCoords, '/damage_image/coords')
