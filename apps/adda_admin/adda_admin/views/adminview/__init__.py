from adda_admin import *
from adda_admin.models.user import user_table
from adda_admin.models.master_config import master_config
from adda_admin.models.internalclaimstatus import internal_claim_status
from adda_admin.models.claim_job import claim_job
from adda_admin.models.externalstatusconfig import external_status_config
from adda_admin.models.uploads import uploads_table
from adda_admin.models.claimsummaryindividual import claim_summary_individual
from adda_admin.models.insurance_vehicle import insurance_vehicle
from adda_admin.models.vehicleassess_parthistory import vehicle_assessment_part_history
from adda_admin.models.vehicleassess_history import vehicle_assessment_history
from adda_admin.models.incs_config import incs_config
from adda_admin.models.client_config import client_config
from adda_admin.models.accesslevel_config import access_level_config
from adda_admin.models.insurance_part import insurance_part
from adda_admin.models.insurance_partdamage import insurance_partdamage
from adda_admin.models.insurance_damage import insurance_damage
from adda_admin.models.insurance_carimage import insurance_carimage
from adda_admin.models.insurance_assess import insurance_assess
from adda_admin.models.claim_summary import claim_summary
from adda_admin.models.parts_name import parts_name
from adda_admin.models.vehicle_type import vehicle_type


from adda_admin.views.adminview.user_view import *
from adda_admin.views.adminview.master_config_view import *
from adda_admin.views.adminview.internalclaimstatus_view import *
from adda_admin.views.adminview.claim_job_view import *
from adda_admin.views.adminview.externalstatusconfig_view import *
from adda_admin.views.adminview.uploads_view import *
from adda_admin.views.adminview.claimsummaryindividual_view import *
from adda_admin.views.adminview.insurance_vehicle_view import *
from adda_admin.views.adminview.vehicleassess_parthistory_view import *
from adda_admin.views.adminview.vehicleassess_history_view import *
from adda_admin.views.adminview.incs_config_view import *
from adda_admin.views.adminview.client_config_view import *
from adda_admin.views.adminview.accesslevel_config_view import *
from adda_admin.views.adminview.insurance_part_view import *
from adda_admin.views.adminview.insurance_partdamage_view import *
from adda_admin.views.adminview.insurance_damage_view import *
from adda_admin.views.adminview.insurance_assess_view import *
from adda_admin.views.adminview.insurance_carimage_view import *
from adda_admin.views.adminview.parts_name_view import *
from adda_admin.views.adminview.claim_summary_view import *
from adda_admin.views.adminview.vehicle_type_view import *


def addAdminView(admin):
	admin.add_view(UserAdminView(user_table, db.session, name="Users"))
	admin.add_view(MasterConfigAdminView(master_config, db.session, name="MasterConfig"))
	admin.add_view(InternalClaimStatusAdminView(internal_claim_status, db.session, name="Incs"))
	admin.add_view(ClaimJobAdminView(claim_job, db.session, name="ClaimJob"))
	admin.add_view(ExternalStatusConfigAdminView(external_status_config, db.session, name="ExtConfig"))
	admin.add_view(UploadsAdminView(uploads_table, db.session, name="Uploads"))
	admin.add_view(ClaimSummaryIndividualAdminView(claim_summary_individual, db.session, name="IndClaimSummary"))
	admin.add_view(InsuranceVehicleAdminView(insurance_vehicle, db.session, name="Vehicle"))
	admin.add_view(VehicleAssessPartHistoryAdminView(vehicle_assessment_part_history, db.session, name="VehicleAssesspartHist"))
	admin.add_view(VehicleAssessHistoryAdminView(vehicle_assessment_history, db.session, name="VehicleAssessHist"))
	admin.add_view(IncsConfigAdminView(incs_config, db.session, name="IncsConfig"))
	admin.add_view(ClientConfigAdminView(client_config, db.session, name="ClientConfig"))
	admin.add_view(AccessLevelConfigAdminView(access_level_config, db.session, name="AccessLevelConfig"))
	admin.add_view(InsurancePartAdminView(insurance_part, db.session, name="Part"))
	admin.add_view(InsurancePartDamageAdminView(insurance_partdamage, db.session, name="PartDamage"))
	admin.add_view(InsuranceDamageAdminView(insurance_damage, db.session, name="Damage"))
	admin.add_view(InsuranceCarimageAdminView(insurance_carimage, db.session, name="CarImage"))
	admin.add_view(InsuranceAssessAdminView(insurance_assess, db.session, name="Assess"))
	admin.add_view(PartsNameAdminView(parts_name, db.session, name="PartsName"))
	admin.add_view(ClaimSummaryAdminView(claim_summary, db.session, name="ClaimSummary"))
	admin.add_view(VehicleTypeAdminView(vehicle_type, db.session, name="VehicleType"))


def addContextProcessor(app):
	@app.context_processor
	def inject_paths():
	    # you will be able to access {{ path1 }} and {{ path2 }} in templates
	    return dict(path1=session.get('access_token', 'not set'), path2='y')











	

	


	

