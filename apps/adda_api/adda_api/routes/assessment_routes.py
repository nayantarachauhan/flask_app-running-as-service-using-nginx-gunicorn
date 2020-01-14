from adda_api.routes import *
from adda_api.views.assessment_api import AssessAll, Assessment, Assessment_update, AssessCompleted, AssessInProcess, AssessFailed, AssessCompletedHil, AssessUpdated, AssessReviewed, AssessClosed


api.add_resource(AssessCompleted, '/assessment_list/completed')
api.add_resource(AssessInProcess, '/assessment_list/in_process')
api.add_resource(AssessFailed, '/assessment_list/failed')
api.add_resource(AssessCompletedHil, '/assessment_list/completed_hil')
api.add_resource(AssessUpdated, '/assessment_list/updated')
api.add_resource(AssessReviewed, '/assessment_list/reviewed')
api.add_resource(AssessClosed, '/assessment_list/closed')

api.add_resource(Assessment, '/assessment')
api.add_resource(AssessAll, '/assessment_list_all')

api.add_resource(Assessment_update, '/assessment/<int:assess_id>/')