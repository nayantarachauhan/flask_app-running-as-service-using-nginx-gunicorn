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
from PIL import Image
from uuid import uuid4
from adda_api.models.insurance_vehicle import insurance_vehicle
from adda_api.models.uploads import uploads_table




class Uploads(Resource):
    @jwt_required
    @checkAccessLevel(access_type = uploads_post)
    def post(self):
        try:

            ACCEPTED_FILE_EXTENSION = ['.jpg', '.jpeg', '.png']

            source_name   = request.form.get("upload[source_name]")
            claim_num     = request.form.get("upload[claim_num]")
            last_image    = request.form.get("upload[last_image]")
            vehicle_type    = request.form.get("upload[vehicle_type]")

            entry = db.session.query(insurance_vehicle.image_count).filter_by(ref_num = claim_num).first()

            if entry:
                return {"Error": "Claim already initiated", "Total_images": entry[0]}

            # paths for images

            upload_path      =  os.path.join(source_name, claim_num, "uploads")
            
            result = {}

            for index in range(len(request.files)):

                # Data extraction from coming from post request

                imageFile     = request.files.get("upload[pictures_attributes][%s][file]" % index)
                imageName     = request.form.get("upload[pictures_attributes][%s][name]" % index)
                imageFileName = request.files.get("upload[pictures_attributes][%s][file]" % index).filename
                
                # split the filename and extension

                image_name, ext  = os.path.splitext(imageFileName)

                if ext not in ACCEPTED_FILE_EXTENSION:
                    result[imageFileName] = "file extention not in [jpg, jpeg, png]"
                    continue

                filename = '%s.jpg' % os.getpid()
                
                imageFile.save(filename)

                try:
                    img = Image.open(filename)

                except:
                    result[imageFileName] = "image is corrupt"
                    os.remove(filename)
                    continue

                width, height = img.size

                if width < 1024 and height < 720:
                    result[imageFileName] = "image resolution less than (1024 X 720)"
                    os.remove(filename)
                    continue

                if not os.path.exists(source_name):
                    os.mkdir(source_name)

                if not os.path.exists(os.path.join(source_name, claim_num)):
                    os.mkdir(os.path.join(source_name, claim_num))

                if not os.path.exists(upload_path):
                    os.mkdir(upload_path)

                uid = uuid4()

                update_filename = "%s.jpg" % str(uid).split("-")[-1]

                path = os.path.join(upload_path, update_filename)

                img.save(path)
                os.remove(filename)

                upload_data = uploads_table(ref_num = claim_num, source_name = source_name, name = imageName, 
                                            picture = path, width = width, height = height)

                db.session.add(upload_data)
                db.session.commit()

            image_count = len(os.listdir(upload_path))
            claim_init_error = ""

            if str(last_image).strip() == '1':
                if image_count >= 6:
                    data = insurance_vehicle(ref_num = claim_num, source_name = source_name, claim_state = "0",
                    image_count = image_count , vehicle_type = vehicle_type.lower())
                    db.session.add(data)
                    db.session.commit()

                else:
                    claim_init_error = "Minimum of 6 images required"
                    last_image = 0

            else:
                last_image = 0
            
            if result and not image_count:
                status = -1

            elif not result and image_count:
                status = 1

            else:
                status = 0

            return {"Upload_error": result, "Successful_uploaded_count": image_count, "Upload_status": status,
            "Claim_init_status": last_image, "Claim_init_error": claim_init_error}

        except Exception as e:
            return {"Error" : str(e)}
            logger.debug("\n------- Something went wrong -------\n", str(e))