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
from adda_api.models.insurance_part import insurance_part



###################################### PARTS CLASS #############################################


class Parts(Resource):
    @jwt_required
    @checkAccessLevel(access_type = part_get)
    def get(self):
        try:
            results = DB_query.get(insurance_part)
            response = {}
            for index, res in enumerate(results):
                response[index] = {
                "id": res.id,
                "ref_num": res.ref_num,
                "side": res.side,
                "name": res.name,
                "full_name": res.full_name,
                "bounds": res.bounds,
                "coordinates": res.coordinates,
                "picture": res.picture,
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
    @checkAccessLevel(access_type = part_delete)
    def delete(self):
        try:
            DB_query.delete(insurance_part)
            return {"result": "Successfully deleted"}
        
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))



class Parts_update(Resource):
    @jwt_required
    @checkAccessLevel(access_type = part_put)
    def put(self, part_id):
        try:
            DB_query.put(part_id, insurance_part)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))

