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
from adda_api.models.insurance_assess import insurance_assess
from adda_api.models.insurance_vehicle import insurance_vehicle
from adda_api.models.insurance_part import insurance_part
from adda_api.models.insurance_partdamage import insurance_partdamage
from adda_api.models.insurance_damage import insurance_damage
from adda_api.models.insurance_carimage import insurance_carimage
from adda_api.models.vehicleassess_history import vehicle_assessment_history
from adda_api.models.vehicleassess_parthistory import vehicle_assessment_part_history
from adda_api.models.claimsummaryindividual import claim_summary_individual




##################################### ASSESSMENT LIST CLASS #############################################


class AssessAll(Resource):
    @jwt_required
    @checkAccessLevel(access_type = assessall_get)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('source_name', type=str, help='source_name is needed!', required = True)
            parser.add_argument('start_date', type=str)
            parser.add_argument('stop_date', type=str)
            args = parser.parse_args()
            
            if args['start_date'] is None and args['stop_date'] is None:
                result = db.session.query(insurance_vehicle).filter(insurance_vehicle.source_name == args['source_name'])

            elif args['stop_date'] is None:
                result = db.session.query(insurance_vehicle).filter(insurance_vehicle.source_name == args['source_name'], insurance_vehicle.created_at >= args['start_date'])

            else:
                result = db.session.query(insurance_vehicle).filter(insurance_vehicle.source_name == args['source_name'], insurance_vehicle.created_at >= args['start_date'],  insurance_vehicle.created_at <= args['stop_date'] )

            response = {}

            for index, res in enumerate(result):
                response[index] = {
                "id": res.id,
                "ref_num": res.ref_num,
                "claim_state": res.claim_state,
                "created_at": str(res.created_at)
                }


            return jsonify(response)

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))


class Assessment(Resource):
    @jwt_required
    @checkAccessLevel(access_type = assessment_get)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('ref_num', type=str, help='ref_num is needed!', required = True)
            parser.add_argument('source_name', type=str, help='source_name is needed!', required = True)
            args = parser.parse_args()

            assess_result        = db.session.query(insurance_assess).filter_by(ref_num = args['ref_num'], source_name = args["source_name"]).order_by(insurance_assess.intensity.desc())
            claim_summary_result = db.session.query(claim_summary_individual).filter_by(ref_num = args['ref_num'], source_name = args["source_name"]).first()
            
            if claim_summary_result:
                claim_summary = {
                "id"              : claim_summary_result.id,
                "ref_num"         : claim_summary_result.ref_num,
                "source_name"     : claim_summary_result.source_name,
                "uploaded"        : claim_summary_result.uploaded,
                "height_width"    : claim_summary_result.height_width,
                "roi"             : claim_summary_result.roi,
                "parts_identified": claim_summary_result.parts_identified,
                "side_left"       : claim_summary_result.side_left,
                "side_right"      : claim_summary_result.side_right,
                "side_front"      : claim_summary_result.side_front,
                "side_rear"       : claim_summary_result.side_rear,
                "side_frontLeft"  : claim_summary_result.side_frontLeft,
                "side_frontRight" : claim_summary_result.side_frontRight,
                "side_rearLeft"   : claim_summary_result.side_rearLeft,
                "side_rearRight"  : claim_summary_result.side_rearRight
                }
            else:
                print("No Data")
                claim_summary = {}

            part_result = db.session.query(insurance_part).filter_by(ref_num = args['ref_num'], source_name = args["source_name"])

            parts = {}

            if part_result.first():

                for index, res in enumerate(part_result):
                    parts[res.id] = {
                    "id"       : res.id,
                    "ref_num"  : res.ref_num,
                    "picture"  : res.picture,
                    "full_name": res.full_name,
                    "side"     : res.side
                    }

            else:
                print("No Data")

            partdamage_result = db.session.query(insurance_partdamage).filter_by(ref_num = args['ref_num'], source_name = args["source_name"])

            partdamages = {}

            if partdamage_result.first():

                for index, res in enumerate(partdamage_result):
                    partdamages[res.id] = {
                    "id"         : res.id,
                    "ref_num"    : res.ref_num,
                    "picture"    : res.picture,
                    "side"       : res.side,
                    "coordinates": res.coordinates,
                    "part_id"    : res.part_id
                    }

            else:
                print("No Data")


            damage_result = db.session.query(insurance_damage).filter_by(ref_num = args['ref_num'], source_name = args["source_name"])

            damages = {}

            if damage_result.first():

                for index, res in enumerate(damage_result):
                    damages[res.id] = {
                    "id"         : res.id,
                    "ref_num"    : res.ref_num,
                    "picture"    : res.picture,
                    "file_name"  : res.file_name,
                    "coordinates": res.original_coordinates
                    }

            else:
                print("No Data")

            carImage_result = db.session.query(insurance_carimage).filter_by(ref_num = args['ref_num'], source_name = args["source_name"])

            carImages = {}

            if carImage_result.first():

                for index, res in enumerate(carImage_result):
                    carImages[res.id] = {
                    "id"         : res.id,
                    "ref_num"    : res.ref_num,
                    "picture"    : res.picture,
                    "name"       : res.name
                    }

            else:
                print("No Data")

            assess_history_result = db.session.query(vehicle_assessment_part_history).filter_by(ref_num = args['ref_num'], source_name = args["source_name"]).order_by(vehicle_assessment_part_history.intensity.desc())

            assess_history = {}

            if assess_history_result.first():

                for index, res in enumerate(assess_history_result):
                    assess_history[res.id] = {
                    "id"                : res.id,
                    "user_id"           : res.user_id,
                    "ref_num"           : res.ref_num,
                    "assess_id"         : res.assess_id,
                    "part_id"           : res.part_id,
                    "partdamage_id"     : res.partdamage_id,
                    "action"            : res.action,
                    "intensity"         : res.intensity,
                    "edited_part_coords": res.edited_part_coords
                    }

            else:
                print("No Data")

            assess_comment_history_result = db.session.query(vehicle_assessment_history).filter_by(ref_num = args['ref_num'], source_name = args["source_name"])

            assess_comment_history = {}

            if assess_comment_history_result.first():

                for index, res in enumerate(assess_comment_history_result):
                    assess_comment_history[res.id] = {
                    "id"         : res.id,
                    "user_id"    : res.user_id,    
                    "ref_num"    : res.ref_num,
                    "comment"    : res.comment,
                    "user_id"    : res.user_id
                    }

            else:
                print("No Data")


            assess = {}

            if assess_result.first():

                for index, res in enumerate(assess_result):
                    assess[index] = {
                    "id": res.id,
                    "action": res.action,
                    "intensity": int(res.intensity),
                    "ref_num": res.ref_num,
                    "part_id": res.part_id,
                    "partdamage_id": res.partdamage_id,
                    "vehicle_id": res.vehicle_id,
                    "used": res.used,
                    "is_fp": res.is_fp
                    }

            else:
                print("No Data")

            return {"claim_summary":claim_summary, "assess": assess, "parts": parts,
                    "partdamages": partdamages, "damages": damages, "carImages":carImages,
                    "assess_history": assess_history, "assess_comment_history":assess_comment_history}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))

    

    @jwt_required
    @checkAccessLevel(access_type = assessment_delete)
    def delete(self):
        try:
            DB_query.delete(insurance_assess)
            return {"result": "Successfully deleted"}
        
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))


class Assessment_update(Resource):
    @jwt_required
    @checkAccessLevel(access_type = assessment_put)
    def put(self, assess_id):
        try:
            DB_query.put(assess_id, insurance_assess)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))


class AssessCompleted(Resource):
    @jwt_required
    @checkAccessLevel(access_type = assesscompleted_get)
    def get(self):

        try:
            results = DB_query.getFromVehicle(insurance_vehicle, "2")
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
            return {"error" : str(e)}


class AssessInProcess(Resource):
    @jwt_required
    @checkAccessLevel(access_type = assessinprocess_get)
    def get(self):

        try:
            results = DB_query.getFromVehicle(insurance_vehicle, "1")
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
            return {"error" : str(e)}



class AssessFailed(Resource):
    @jwt_required
    @checkAccessLevel(access_type = assessfailed_get)
    def get(self):

        try:
            results = DB_query.getFromVehicle(insurance_vehicle, "6")
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
            return {"error" : str(e)}



class AssessCompletedHil(Resource):
    @jwt_required
    @checkAccessLevel(access_type = assesscompletedhil_get)

    def get(self):

        try:
            results = DB_query.getFromVehicle(insurance_vehicle, "3")
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
            return {"error" : str(e)}


class AssessUpdated(Resource):
    @jwt_required
    @checkAccessLevel(access_type = assessupdated_get)
    def get(self):

        try:
            results = DB_query.getFromVehicle(insurance_vehicle, "4")
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
            return {"error" : str(e)}


class AssessReviewed(Resource):
    @jwt_required
    @checkAccessLevel(access_type = assessreviewed_get)
    def get(self):

        try:
            results = DB_query.getFromVehicle(insurance_vehicle, "5")
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
            return {"error" : str(e)}


class AssessClosed(Resource):
    @jwt_required
    @checkAccessLevel(access_type = assessclosed_get)
    def get(self):

        try:
            results = DB_query.getFromVehicle(insurance_vehicle, "7")
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
            return {"error" : str(e)}
