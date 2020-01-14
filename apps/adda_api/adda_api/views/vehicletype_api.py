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
from adda_api.models.vehicle_type import vehicle_type



############################ vehicle_type####################################



class VehicleType(Resource):
    @jwt_required
    @checkAccessLevel(access_type = vehicletype_get )
    def get(self):

        try:
            results = db.session.query(vehicle_type).all()

            response = {}

            for index, res in enumerate(results):
                response[index] = {
                "id": res.id,
                "vehicle_type": res.vehicle_type,
                "tyres_count": res.tyres_count

                }

            print(response)

            return jsonify(response)

        except Exception as e:
            return {"error" : str(e)}


    @jwt_required
    @checkAccessLevel(access_type = vehicletype_delete )
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('vehicle_type', type=str, help='vehicle_type is needed!', required = True)
            args = parser.parse_args()

            db.session.query(vehicle_type).filter(vehicle_type.vehicle_type == args['vehicle_type']).delete(synchronize_session=False)
            db.session.commit()

            return {"result": "Successfully deleted"}
        
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))


    @jwt_required
    @checkAccessLevel(access_type = vehicletype_post)
    def post(self):

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('vehicle_type', type=str, help='vehicle_type ', required = True)
            parser.add_argument('tyres_count', type=str, help='tyres_count' , required = True)
            args = parser.parse_args()
            new_data = vehicle_type(vehicle_type = args['vehicle_type'], tyres_count = args['tyres_count'])
            db.session.add(new_data)
            db.session.commit()
            return {"status" : "successfully inserted values in database"}
                
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))



class VehicleType_update(Resource):
    @jwt_required
    @checkAccessLevel(access_type = vehicletype_put)
    def put(self, id):        
        try:
            DB_query.put(id, vehicle_type)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))
