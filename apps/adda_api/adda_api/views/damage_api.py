
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
from adda_api.models.insurance_damage import insurance_damage




###################################### DAMAGE CLASS #############################################

class Damages(Resource):
    @jwt_required
    @checkAccessLevel(access_type = damage_get)
    def get(self):
        try:
            results = DB_query.get(insurance_damage)
            response = {}
            for index, res in enumerate(results):
                response[index] = {
                "id": res.id,
                "side": res.side,
                "ref_num": res.ref_num,
                "bounds": res.bounds,
                "original_coordinates": res.original_coordinates,
                "edited_coordinates": res.edited_coordinates,
                "picture" : res.picture,
                "created_at": res.created_at,
                "updated_at": res.updated_at,
                "vehicle_id": res.vehicle_id,
                "file_name": res.file_name
                }
            return jsonify(response)

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))



    @jwt_required
    @checkAccessLevel(access_type = damage_delete)
    def delete(self):
        try:
            DB_query.delete(insurance_damage)
            return {"result": "Successfully deleted"}
        
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))



class Damages_update(Resource):
    @jwt_required
    @checkAccessLevel(access_type = damage_put)
    def put(self, damage_id):
        try:
            DB_query.put(damage_id, insurance_damage)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))
