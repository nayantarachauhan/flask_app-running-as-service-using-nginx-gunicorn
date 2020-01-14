from adda_admin import Base, login_manager, db
from flask_login import UserMixin

############################ TABLES ########################################


class user(Base, UserMixin):
    __tablename__ = 'user'

user_table = user

@login_manager.user_loader
def load_user(id):
    return db.session.query(user_table).get(int(id))