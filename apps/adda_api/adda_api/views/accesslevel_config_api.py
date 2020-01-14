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
from adda_api.models.accesslevel_config import access_level_config



############################ access_level_config####################################


class AccessLevelConfig(Resource):
    @jwt_required
    @checkAccessLevel(access_type = accesslevel_config_get)
    def get(self):

        try:
            results = db.session.query(access_level_config).all()

            response = {}

            for index, res in enumerate(results):
                response[index] = {
                "id": res.id,
                "access_level_name": res.access_level_name,
                "access_level_flag": res.access_level_flag

                }

            return jsonify(response)

        except Exception as e:
            return {"error" : str(e)}


    @jwt_required
    @checkAccessLevel(access_type = accesslevel_config_delete)
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('access_level_flag', type=str, help='access_level_flag!', required = True)
            args = parser.parse_args()

            db.session.query(access_level_config).filter(access_level_config.access_level_flag == args['access_level_flag']).delete(synchronize_session=False)
            db.session.commit()

            return {"result": "Successfully deleted"}
            
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))


    
    @jwt_required
    @checkAccessLevel(access_type = accesslevel_config_post)
    def post(self):

        try:
            print("------------------")
            parser = reqparse.RequestParser()
            print("------------------")
            parser.add_argument('access_level_name', type=str, help='access_level_name ', required = True)
            parser.add_argument('access_level_flag', type=str, help='access_level_flag' , required = True)
            args = parser.parse_args()
            print("args-------", args)
            new_data = access_level_config(access_level_name = args['access_level_name'], access_level_flag = args['access_level_flag'])
            db.session.add(new_data)
            db.session.commit()
            return {"status" : "successfully inserted values in database"}
                
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))



class AccessLevelConfig_update(Resource):
    @jwt_required
    @checkAccessLevel(access_type = accesslevel_config_put)
    def put(self, id):        
        try:
            DB_query.put(id, access_level_config)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))
