from adda_api.routes import *
from adda_api.views.partdamage_api import PartDamage, PartDamage_update

api.add_resource(PartDamage, '/part_damage')
api.add_resource(PartDamage_update, '/part_damage/<int:partdamage_id>/')

