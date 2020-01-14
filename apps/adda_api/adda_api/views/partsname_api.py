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
from adda_api.models.parts_name import parts_name



############################ parts_name####################################


class PartsName(Resource):
    @jwt_required
    @checkAccessLevel(access_type = partsname_get)
    def get(self):

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('vehicle_type_id', type=str, help='vehicle_type_id is needed!', required = True)
            args = parser.parse_args()
            results = db.session.query(parts_name).filter_by(vehicle_type_id =args['vehicle_type_id'])

            response = {}

            for index, res in enumerate(results):
                response[index] = {
                "id": res.id,
                "part_name": res.part_name,
                "part_full_name": res.part_full_name,
                "part_side": res.part_side,
                "vehicle_type_id": res.vehicle_type_id,
                "assess_flag": res.assess_flag,
                "nodamage_flag": res.nodamage_flag
                }

            return jsonify(response)

        except Exception as e:
            return {"error" : str(e)}


    @jwt_required
    @checkAccessLevel(access_type = partsname_delete)
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('part_full_name', type=str, help='part_full_name is needed!', required = True)
            args = parser.parse_args()

            db.session.query(parts_name).filter(parts_name.part_full_name == args['part_full_name']).delete(synchronize_session=False)
            db.session.commit()

            return {"result": "Successfully deleted"}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))


    @jwt_required
    @checkAccessLevel(access_type = partsname_post)
    def post(self):

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('part_name', type=str, help='part_name ', required = True)
            parser.add_argument('part_full_name', type=str, help='part_full_name' , required = True)
            parser.add_argument('part_side', type=str, help='part_side' , required = True)
            parser.add_argument('vehicle_type_id', type=str, help='vehicle_type_id' , required = True)
            parser.add_argument('nodamage_flag', type=str, help='nodamage_flag' , required = True)
            parser.add_argument('assess_flag', type=str, help='assess_flag' , required = True)
            args = parser.parse_args()
            new_data = parts_name(part_name = args['part_name'], part_full_name = args['part_full_name'] , part_side = args['part_side'] , vehicle_type_id = args['vehicle_type_id'] , nodamage_flag = args['nodamage_flag'] , assess_flag = args['assess_flag'])
            db.session.add(new_data)
            db.session.commit()
            return {"status" : "successfully inserted values in database"}
                
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))



class PartsName_update(Resource):
    @jwt_required
    @checkAccessLevel(access_type = partsname_put)
    def put(self, id):        
        try:
            DB_query.put(id, parts_name)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))
