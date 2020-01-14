
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
from adda_api.models.insurance_vehicle import insurance_vehicle
from adda_api.models.insurance_part import insurance_part
from adda_api.models.insurance_partdamage import insurance_partdamage
from adda_api.models.insurance_damage import insurance_damage
from adda_api.models.insurance_assess import insurance_assess
from adda_api.models.insurance_carimage import insurance_carimage


################################# VEHICLE CLASS ##############################################


class Vehicle(Resource):
    @jwt_required
    @checkAccessLevel(access_type = vehicle_get)
    def get(self):

        try:

            results = DB_query.get(insurance_vehicle)
            response = {}

            for index, res in enumerate(results):
                response[index] = {
                "id": res.id,
                "ref_num": res.ref_num,
                "make": res.make,
                "model": res.model,
                "score": res.score,
                "result": res.result,
                "num_plate": res.num_plate,
                "comment": res.comment,
                "created_at": str(res.created_at),
                "updated_at": str(res.updated_at),
                "source_name": res.source_name,
                "claim_state": res.claim_state,
                "user_id": res.user_id,
                "image_count": res.image_count,
                "reviewer_comment": res.reviewer_comment
                }

            return jsonify(response)

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))

    

    @jwt_required
    @checkAccessLevel(access_type = vehicle_post)
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('ref_num', type=str, help='claim_id')
            parser.add_argument('image_count', type=str, help='count of uploaded image')
            parser.add_argument('claim_state', type=str, help='state of the claim')
            parser.add_argument('source_name', type=str, help='source_name')
            args = parser.parse_args()
            new_data = insurance_vehicle(ref_num = args['ref_num'], image_count = args['image_count'], claim_state= args['claim_state'], source_name = args['source_name'], created_at = str(datetime.now()), updated_at = str(datetime.now()))
            db.session.add(new_data)
            db.session.commit()
            return {"status" : "successfully inserted values in database"}
            
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))


    @jwt_required
    @checkAccessLevel(access_type = vehicle_delete)
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('ref_num', type=str, help='ref_num is needed!', required = True)
            parser.add_argument('source_name', type=str, help='source_name is needed!', required = True)
            args = parser.parse_args()

            vehicle = db.session.query(insurance_vehicle.id).filter(insurance_vehicle.ref_num == args['ref_num'], 
                       insurance_vehicle.source_name == args['source_name'])[0]
            
            vehicle_id = vehicle.id

            db.session.query(insurance_assess).filter(insurance_assess.ref_num == args['ref_num']).delete(synchronize_session=False)
            db.session.query(insurance_carimage).filter(insurance_carimage.ref_num == args['ref_num']).delete(synchronize_session=False)
            db.session.query(insurance_damage).filter(insurance_damage.ref_num == args['ref_num']).delete(synchronize_session=False)
            # db.session.query(insurance_image).filter(insurance_image.ref_num == args['ref_num']).delete(synchronize_session=False)
            db.session.query(insurance_partdamage).filter(insurance_partdamage.vehicle_id == vehicle_id).delete(synchronize_session=False)
            db.session.query(insurance_part).filter(insurance_part.ref_num == args['ref_num']).delete(synchronize_session=False)

            db.session.query(insurance_vehicle).filter(insurance_vehicle.ref_num == args['ref_num'], 
                       insurance_vehicle.source_name == args['source_name']).delete(synchronize_session=False)
            db.session.commit()

            return {"result": "Successfully deleted"}
        
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))


class Vehicle_update(Resource):
    @jwt_required
    @checkAccessLevel(access_type = vehicle_put)
    def put(self, vehicle_id):        
        try:
            DB_query.put(vehicle_id, insurance_vehicle)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))

