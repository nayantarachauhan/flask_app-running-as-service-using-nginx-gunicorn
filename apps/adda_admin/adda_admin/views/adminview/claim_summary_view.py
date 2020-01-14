from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from adda_admin import login_manager

class ClaimSummaryAdminView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated