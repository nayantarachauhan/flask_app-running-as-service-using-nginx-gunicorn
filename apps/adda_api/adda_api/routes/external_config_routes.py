from adda_api.routes import *
from adda_api.views.external_config_api import ExternalConfig_update, ExternalConfig

api.add_resource(ExternalConfig,'/external_config')
api.add_resource(ExternalConfig_update,'/external_config/<int:id>/')
