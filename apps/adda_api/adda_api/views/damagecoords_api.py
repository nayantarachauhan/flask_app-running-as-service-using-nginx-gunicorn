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
from adda_api.models.insurance_damage import insurance_damage


class DamageCoords(Resource):
    @jwt_required
    @checkAccessLevel(access_type = damagecoords_get)
    def get(self):
        try:            
            results = DB_query.get(insurance_damage)

            response = {}

            for index, res in enumerate(results):
                print(res.ref_num)
                path = "media/car_image/" + res.ref_num + '/' + res.file_name

                response[index] = {
                "coordinates": res.original_coordinates,
                "image_path": path,
                }

            return jsonify(response)

        except Exception as e:
            return {"error" : str(e)}