from adda_admin.routes import *
from adda_admin.views.user_registerNlogin import Auth


###########Route

api.add_resource(Auth,'/auth/')





