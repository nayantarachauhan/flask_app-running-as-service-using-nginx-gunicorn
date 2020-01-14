from adda_api.routes import *
from adda_api.views.uploads_api import Uploads


api.add_resource(Uploads, '/uploads')
