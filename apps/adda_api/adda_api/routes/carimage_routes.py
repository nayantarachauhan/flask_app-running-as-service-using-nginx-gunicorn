from adda_api.routes import *
from adda_api.views.carimage_api import CarImage, CarImage_update


api.add_resource(CarImage,  '/car_image')
api.add_resource(CarImage_update,   '/car_image/<int:carimage_id>/')
