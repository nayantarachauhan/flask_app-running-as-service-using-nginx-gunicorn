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
from adda_api.models.insurance_partdamage import insurance_partdamage
from adda_api.models.insurance_vehicle import insurance_vehicle




###################################### PARTDAMAGE  CLASS #############################################


class PartDamage(Resource):
    @jwt_required
    @checkAccessLevel(access_type = partdamage_get)
    def get(self):

        try:

            results = DB_query.get(insurance_partdamage)
            # print("results--------",results)
            response = {}

            for index, res in enumerate(results):
                response[index] = {
                "id": res.id,
                "side": res.side,
                "ref_num": res.ref_num,
                "part_name": res.part_name,
                "coordinates": res.coordinates,
                "picture": res.picture,
                "intensity": res.intensity,
                "created_at": str(res.created_at),
                "updated_at": str(res.updated_at),
                "part_id": res.part_id,
                "vehicle_id": res.vehicle_id,
                "file_name": res.file_name,
                "is_fp": res.is_fp,
                "source_name" : res.source_name
                }

            return jsonify(response)

        except Exception as e:
            return {"error" : str(e)}


    @jwt_required
    @checkAccessLevel(access_type = partdamage_delete)
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('ref_num', type=str, help='ref_num is needed!', required = True)
            parser.add_argument('source_name', type=str, help='source_name is needed!', required = True)
            args = parser.parse_args()

            vehicle = db.session.query(insurance_vehicle.id).filter(insurance_vehicle.ref_num == args['ref_num'], 
                       insurance_vehicle.source_name == args['source_name'])[0]
            
            vehicle_id = vehicle.id

            # db.session.query(table).filter(table.ref_num == args['ref_num'], table.source_name == args['source_name']).delete(synchronize_session=False)
            db.session.query(insurance_partdamage).filter(insurance_partdamage.vehicle_id == vehicle_id).delete(synchronize_session=False)
            db.session.commit()

            return {"result": "Successfully deleted"}
        
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))



class PartDamage_update(Resource):
    @jwt_required
    @checkAccessLevel(access_type = partdamage_put)
    def put(self, partdamage_id):
        try:
            DB_query.put(partdamage_id, insurance_partdamage)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))