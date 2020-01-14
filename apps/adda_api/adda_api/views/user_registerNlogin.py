import os, json
from datetime import datetime, timedelta
from flask import request,render_template, Response,redirect, url_for,jsonify #,session
from flask_restful import Resource
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import functools
from adda_api import *
from adda_api.utility.validate_user import validate_user
from adda_api.configuration.api_access_config import *
from adda_api.models.user import user_table



############################# Check Access Level #################################

def checkAccessLevel(_func=None, *, access_type=["1"]):
    def actualCheck(func):
        @functools.wraps(func)
        def accesslevels(*args, **kwargs):
            token_identity = get_jwt_identity()
            print("token identity -----------------: ",token_identity)
            print("access type -----------------: ",access_type)

            if ( token_identity['access_level'] in access_type ):
                return func(*args,**kwargs)
            else:
                return "you do not have authorization!!!", 401
        return accesslevels

    if _func is not None:
        return actualCheck(_func)
    else:
        return actualCheck



class LoginForm(FlaskForm):
    email = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


###################### auth #########################3

class Auth(Resource):
    def get(self):
        if not current_user.is_authenticated:
            form = LoginForm()
            return Response(render_template('auth.html', form=form), content_type='text/html')
        else:
            return redirect(url_for('admin.index'))

    def post(self):
        data = request.form
        data = validate_user(data)

        if data['ok']:
            data = data['data']
            email = data['email']
            password = data['password']

            try:
                results = db.session.query(user_table).filter(user_table.email_id == email)
                response = {}
                for index, res in enumerate(results):
                    response[index] = {
                    "id": res.id,
                    "username": res.username,
                    "email_id": res.email_id,
                    "password": res.password,
                    "access_level": res.access_level,
                    "flag": res.flag
                    }
                
                db_password = response[0]['password']
                db_username = response[0]['username']
                db_access_level = response[0]['access_level']
                db_id = response[0]['id']

                password_verf = flask_bcrypt.check_password_hash(db_password, password)
                if password_verf == True and db_access_level == "0"  :
                    del db_password
                    data = {'username' : db_username, 'access_level': db_access_level}
                    access_token = create_access_token(identity=data)
                    user1  = db.session.query(user_table).get(db_id)

                    login_user(user1)
                    session['access_token'] = access_token
                    return redirect(url_for('admin.index'))
                else:
                    return jsonify({'message': 'wrong password or you are not the admin'})


            
            except Exception as e:
                return {"Error" : str(e), "msg": "This mail id is not registered"}

        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])})

        
        

####################################    LOGIN   #######################################

class Login(Resource):

    def post(self):
        
        data = request.form
        data = validate_user(data)

        if data['ok']:
            data = data['data']
            email = data['email']
            password = data['password']

            try:
                results = db.session.query(user_table).filter(user_table.email_id == email)
                response = {}
                for index, res in enumerate(results):
                    response[index] = {
                    "id": res.id,
                    "username": res.username,
                    "email_id": res.email_id,
                    "password": res.password,
                    "access_level": res.access_level,
                    "flag": res.flag
                    }
                
                db_password = response[0]['password']
                db_username = response[0]['username']
                db_access_level = response[0]['access_level']

                password_verf = flask_bcrypt.check_password_hash(db_password, password)
                if password_verf == True  :
                    del db_password
                    data = {'username' : db_username, 'access_level': db_access_level}
                    access_token = create_access_token(identity=data)
                    return jsonify({'token' : access_token})
                else:
                    return jsonify({'message': 'wrong password'})


            
            except Exception as e:
                return {"Error" : str(e), "msg": "This mail id is not registered"}

        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])})



#################################################registration ###############################################

class Register(Resource):

    def post(self):

        data = request.form

        print(data)

        data = validate_user(data)

        if data['ok']:
            data = data['data']
            email = data['email']
            results = db.session.query(user_table).filter(user_table.email_id == email).first()
    
            if results:
                return jsonify({'message': 'This mail id is already registered!'})
            
            else:
                password = flask_bcrypt.generate_password_hash(data['password']).decode("utf8")
                try:
                    new_data = user_table(username = data['name'], email_id = data['email'], password = password, access_level = data["access_level"])
                    db.session.add(new_data)
                    db.session.commit()

                except Exception as e:
                    return {"Error" : str(e)}

                return jsonify({'ok': True, 'message': 'User created successfully!'})
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


