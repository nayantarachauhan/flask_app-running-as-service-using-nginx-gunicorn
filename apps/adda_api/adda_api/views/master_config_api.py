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
from adda_api.models.master_config import master_config


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("master config post1........", master_config_post)

############################# master_config#######################################

class MasterConfig(Resource):
    @jwt_required
    @checkAccessLevel(access_type = master_config_get )
    def get(self):
        try:
            global master_config
            results = db.session.query(master_config).all()

            response = {}

            for index, res in enumerate(results):
                response[index] = {
                "id": res.id,
                "meta_name": res.meta_name,
                "meta_value": res.meta_value,
                "enviornment": res.enviornment
                }

            return jsonify(response)

        except Exception as e:
           return {"error" : str(e)}



    @jwt_required
    @checkAccessLevel(access_type = master_config_delete)
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('meta_name', type=str, help='meta_name', required = True)
            parser.add_argument('enviornment', type=str, help='enviornment', required = True)
            args = parser.parse_args()

            db.session.query(master_config).filter(master_config.meta_name == args['meta_name'], master_config.enviornment == args['enviornment']).delete(synchronize_session=False)
            db.session.commit()

            return {"result": "Successfully deleted"}
            
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))



    @jwt_required
    @checkAccessLevel(access_type = master_config_post)

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('meta_name', type=str, help='meta_name ', required = True)
            parser.add_argument('meta_value', type=str, help='meta_value' , required = True)
            parser.add_argument('enviornment', type=str, help='enviornment' , required = True)

            args = parser.parse_args()
            new_data = master_config(meta_name = args['meta_name'], meta_value = args['meta_value'], enviornment = args['enviornment'])
            db.session.add(new_data)
            db.session.commit()
            return {"status" : "successfully inserted values in database"}
                
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))




#################################################################################
# PUT: UPDATE DATA IN DATABASE 
#################################################################################

class MasterConfig_update(Resource):

    @jwt_required
    @checkAccessLevel(access_type = master_config_put)
    def put(self, id):        
        try:
            DB_query.put(id, master_config)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))







