from adda_api.routes import *
from adda_api.views.part_api import Parts, Parts_update

api.add_resource(Parts,'/parts')
api.add_resource(Parts_update,'/parts/<int:part_id>/')