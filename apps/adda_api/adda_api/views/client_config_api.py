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
from adda_api.models.client_config import client_config



############################ client_config ####################################


class ClientConfig(Resource):
    @jwt_required
    @checkAccessLevel(access_type = client_config_get)
    def get(self):

        try:
            results = db.session.query(client_config).all()
            response = {}

            for index, res in enumerate(results):
                response[index] = {
                "id": res.id,
                "source_name": res.source_name,
                "upload_image_count": res.upload_image_count,
                "relevant_image_count": res.relevant_image_count,
                "height": res.height,
                "width": res.width

                }
            

            return jsonify(response)

        except Exception as e:
            return {"error" : str(e)}



    @jwt_required
    @checkAccessLevel(access_type = client_config_delete)
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('source_name', type=str, help='source_name is needed!', required = True)
            parser.add_argument('vehicle_type', type=str, help='vehicle_type is needed!', required = True)
            
            args = parser.parse_args()

            db.session.query(client_config).filter(client_config.source_name == args['source_name'], client_config.vehicle_type == args['vehicle_type']).delete(synchronize_session=False)
            db.session.commit()

            return {"result": "Successfully deleted"}
        
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))

    
    
    @jwt_required
    @checkAccessLevel(access_type = client_config_post)
    def post(self):

        try:
            parser = reqparse.RequestParser()
            parser.add_argument('height', type=str, help='height of image', required = True)
            parser.add_argument('width', type=str, help='width of image' , required = True)
            parser.add_argument('upload_image_count', type=str, help='count of uploaded image' , required = True)
            parser.add_argument('relevant_image_count', type=str, help='count of relevant image' , required = True)
            parser.add_argument('side_count', type=str, help='side_count' , required = True)
            parser.add_argument('vehicle_type_id', type=str, help='vehicle_type_id' , required = True)
            parser.add_argument('source_name', type=str, help='source_name' , required = True)
            args = parser.parse_args()
            new_data = client_config(source_name = args['source_name'], upload_image_count = args['upload_image_count'],relevant_image_count = args['relevant_image_count'], height = args['height'], width = args['width'], vehicle_type_id = args['vehicle_type_id'],side_count = args['side_count'])
            db.session.add(new_data)
            db.session.commit()
            return {"status" : "successfully inserted values in database"}
                
        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))



class ClientConfig_update(Resource):
    
    @jwt_required
    @checkAccessLevel(access_type = client_config_put)
    def put(self, id):        
        try:
            DB_query.put(id, client_config)
            return {"status": 'success'}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))
