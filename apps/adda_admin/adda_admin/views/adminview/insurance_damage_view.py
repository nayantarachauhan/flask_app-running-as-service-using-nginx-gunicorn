from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from adda_admin import login_manager
from flask import Markup


class InsuranceDamageAdminView(ModelView):
	column_searchable_list = ['ref_num']
	column_exclude_list = ["vehicle_id","insurance_vehicle"]

	def is_accessible(self):
		return current_user.is_authenticated

	# def formatter(view, context, model, name):
	# 	print(name)
	# 	print(model)

	def get_list_value(context,model,name):
		if name == 'picture':
			return Markup("<img style='height:200px' src='%s' />" % model.picture)
		else:
			return model.__dict__[name]
