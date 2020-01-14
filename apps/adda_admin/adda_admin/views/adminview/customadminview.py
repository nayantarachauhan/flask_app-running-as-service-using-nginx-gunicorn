from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import redirect, url_for

class AdminIndex(AdminIndexView):
	@expose('/')
	def index(self):
		if not current_user.is_authenticated:
			return redirect(url_for('api.auth'))
		return super(AdminIndex, self).index()