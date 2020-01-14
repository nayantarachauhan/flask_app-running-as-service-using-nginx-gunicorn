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
from adda_api.models.externalstatusconfig import external_status_config



############################# external_config#######################################

class ExternalConfig(Resource):
    @jwt_required
    @checkAccessLevel(access_type = external_config_get)
    def get(self):

        try:
            results = db.session.query(external_status_config).all()

            response = {}

            for index, res in enumerate(results):
                response[index] = {
                "id": res.id,
                "ext_config_name": res.ext_config_name,
                "ext_config_flag": res.ext_config_flag

                }

            return jsonify(response)

        except Exception as e:
            return {"error" : str(e)}


    @jwt_required
    @checkAccessLevel(access_type = external_config_delete)
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('ext_config_flag', type=str, help='ext_config_flag', required = True)
            args = parser.parse_args()

            db.session.query(external_status_config).filter(external_status_config.ext_config_flag == args['ext_config_flag']).delete(synchronize_session=False)
            db.session.commit()

            return {"result": "Successfully deleted"}
            
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))




    @jwt_required
    @checkAccessLevel(access_type = external_config_post)
    def post(self):

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('ext_config_name', type=str, help='ext_config_name ', required = True)
            parser.add_argument('ext_config_flag', type=str, help='ext_config_flag' , required = True)
            args = parser.parse_args()
            new_data = external_status_config(ext_config_name = args['ext_config_name'], ext_config_flag = args['ext_config_flag'])
            db.session.add(new_data)
            db.session.commit()
            return {"status" : "successfully inserted values in database"}
                
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))


class ExternalConfig_update(Resource):
    @jwt_required
    @checkAccessLevel(access_type = external_config_put)
    def put(self, id):        
        try:
            DB_query.put(id, external_status_config)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))
