from adda_api.routes import *
from adda_api.views.accesslevel_config_api import AccessLevelConfig_update, AccessLevelConfig


api.add_resource(AccessLevelConfig,'/access_level_config')
api.add_resource(AccessLevelConfig_update, '/access_level_config/<int:id>/')

