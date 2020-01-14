from adda_api.routes import *
from adda_api.views.master_config_api import MasterConfig_update, MasterConfig


############## Route
api.add_resource(MasterConfig_update, '/master_config/<int:id>/')
api.add_resource(MasterConfig,'/master_config')


