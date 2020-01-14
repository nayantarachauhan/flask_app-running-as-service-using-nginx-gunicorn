from adda_api.routes import *
from adda_api.views.user_registerNlogin import Login, Register,Auth


###########Route

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Auth,'/auth/')





