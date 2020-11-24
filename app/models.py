from . import db
from werkzeug.security import generate_password_hash
import flask_login



class User(flask_login.UserMixin):


    def __init__(self,user_id,first_name,last_name,email_address,telephone,dob):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.telephone = telephone
        self.dob = dob

    def get_id(self):
        return str(self.user_id)
    
    def __repr__(self):
        return '<User %r>' % self.user_id



class Login(flask_login.UserMixin):

    def __init__(self,user_id,username,password):
        self.user_id = user_id
        self.username = username
        self.password = password

    
    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
            

    def get_id(self):
        return str(self.user_id)
    
    def __repr__(self):
        return '<Login %r>' % self.username 

def check_user(id):
        result=db.session.execute("""SELECT user_id, username,password FROM login WHERE user_id=:user_id """,
        {"user_id":id})
        if (result.rowcount):
            for i in result:
                user_id = i[0]
                username = i[1]
                password = i[2]

            return Login(user_id,username,password)
            db.session.close()
        else:
            return None