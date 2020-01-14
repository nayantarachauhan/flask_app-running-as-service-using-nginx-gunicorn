from adda_api.routes import *
from adda_api.views.client_config_api import ClientConfig_update, ClientConfig


api.add_resource(ClientConfig,'/client_config')
api.add_resource(ClientConfig_update, '/client_config/<int:id>/')

