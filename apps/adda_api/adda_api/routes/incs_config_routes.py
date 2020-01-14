from adda_api.routes import *
from adda_api.views.incs_config_api import IncsConfig_update, IncsConfig


api.add_resource(IncsConfig,'/incs_config')
api.add_resource(IncsConfig_update, '/incs_config/<int:id>/')
