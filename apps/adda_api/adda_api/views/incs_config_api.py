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
from adda_api.models.incs_config import incs_config


############################# incs_config#######################################

class IncsConfig(Resource):
    
    @jwt_required
    @checkAccessLevel(access_type = incs_config_get )
    def get(self):

        try:
            results = db.session.query(incs_config).all()

            response = {}

            for index, res in enumerate(results):
                response[index] = {
                "id": res.id,
                "incs_config_name": res.incs_config_name,
                "incs_config_flag": res.incs_config_flag

                }

            return jsonify(response)

        except Exception as e:
            return {"error" : str(e)}


    @jwt_required
    @checkAccessLevel(access_type = incs_config_delete )
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('incs_config_flag', type=str, help='incs_config_flag', required = True)
            args = parser.parse_args()

            db.session.query(incs_config).filter(incs_config.incs_config_flag == args['incs_config_flag']).delete(synchronize_session=False)
            db.session.commit()

            return {"result": "Successfully deleted"}
            
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))



    @jwt_required
    @checkAccessLevel(access_type = incs_config_post )
    def post(self):

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('incs_config_name', type=str, help='incs_config_name ', required = True)
            parser.add_argument('incs_config_flag', type=str, help='incs_config_flag' , required = True)
            args = parser.parse_args()
            new_data = incs_config(incs_config_name = args['incs_config_name'], incs_config_flag = args['incs_config_flag'])
            db.session.add(new_data)
            db.session.commit()
            return {"status" : "successfully inserted values in database"}
                
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))



class IncsConfig_update(Resource):

    @jwt_required
    @checkAccessLevel(access_type = incs_config_put)
    def put(self, id):        
        try:
            DB_query.put(id, incs_config)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))
