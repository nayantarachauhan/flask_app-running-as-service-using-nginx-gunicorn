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
from adda_api.models.claim_summary import claim_summary


class AssessReport(Resource):

    def get(self):

        try:
            res = DB_query.getAssessReport(claim_summary).first()

            try:

                print("res in try----", res.total_claims)
                
                response = {
                    "total_claims": res.total_claims,
                    "completed": res.completed,
                    "failed": res.failed
                    }

                print("response-----------------------",response)

            except:
                print("res in except ----", res[0])

                response = {
                    "total_claims": str(res[0]),
                    "completed": str(res[1]),
                    "failed": str(res[2])
                    }

                print("response of except-----------------------",response)

            return jsonify(response)

        except Exception as e:
            return {"error" : str(e)}