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
from adda_api.models.insurance_partdamage import insurance_partdamage
from adda_api.models.insurance_part import insurance_part




class PartDamageCoords(Resource):
    @jwt_required
    @checkAccessLevel(access_type = partdamagecoords_get )
    def get(self):

        try:
            results = DB_query.get(insurance_partdamage)
            print("results------------", results)

            response = {}

            for index, res in enumerate(results):
                part_id = res.part_id
                result_part = db.session.query(insurance_part.picture).filter_by(id = part_id)
                response[index] = {
                "coordinates": res.coordinates,
                "image_path": result_part[0].picture,
                }

            return jsonify(response)

        except Exception as e:
            return {"error" : str(e)}