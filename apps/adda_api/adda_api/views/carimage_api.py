
import os, json
from flask import request, Request
from flask_restful import Resource
from flask import jsonify
import logging
from flask_restful import reqparse
from adda_api import *
from adda_api.configuration.api_access_config import *
from adda_api.views.user_registerNlogin import checkAccessLevel
from adda_api.utility.common_db_functions import DB_query
from adda_api.models.insurance_carimage import insurance_carimage




################################# CARIMAGE CLASS ##############################################

class CarImage(Resource):
    @jwt_required
    @checkAccessLevel(access_type = carimage_get)
    def get(self):
        try:
            results = DB_query.get(insurance_carimage)
            response = {}
            for index, res in enumerate(results):
                response[index] = {
                "id": res.id,
                "name": res.name,
                "ref_num": res.ref_num,
                "picture": res.picture,
                "created_at": res.created_at,
                "updated_at": res.updated_at,
                "vehicle_id": res.vehicle_id,
                "side": res.side
                }
            return jsonify(response)

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))



    @jwt_required
    @checkAccessLevel(access_type = carimage_delete)
    def delete(self):
        try:
            DB_query.delete(insurance_carimage)
            return {"result": "Successfully deleted"}
        
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))


class CarImage_update(Resource):
    @jwt_required
    @checkAccessLevel(access_type = carimage_put)
    def put(self, carimage_id):
        try:
            DB_query.put(carimage_id, insurance_carimage)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))
