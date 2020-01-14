from adda_api.routes import *
from adda_api.views.assessreport_api import AssessReport


api.add_resource(AssessReport, '/assessment_report')

