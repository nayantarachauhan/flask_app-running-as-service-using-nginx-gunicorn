from adda_api.routes import *
from adda_api.views.damage_api import Damages, Damages_update


api.add_resource(Damages_update, '/damages/<int:damage_id>/')
api.add_resource(Damages, '/damages')

