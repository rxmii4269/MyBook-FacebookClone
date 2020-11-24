from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, PasswordField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email, InputRequired
from wtforms.fields.html5 import DateField


class RegisterForm(FlaskForm):
    username = TextField('Username',validators=[DataRequired(),InputRequired()])
    password = PasswordField('Passwors',validators=[InputRequired()])
    firstname = TextField('First Name',validators=[DataRequired(),InputRequired()])
    lastname = TextField('Last Name',validators=[DataRequired(),InputRequired()])
    email = TextField('Email Address',validators=[DataRequired(),Email()])
    photo = FileField('Add Profile Picture ',validators=[FileRequired(),FileAllowed(['jpg','jpeg','png'],'Images Only!')])
    dob = TextField('Date of Birth',validators=[DataRequired()])
    gender = SelectField('Gender',choices=[('M','Male'),('F','Female'),('Other','Other')],validators=[DataRequired()])
    telephone = TextField('Mobile Number',validators=[DataRequired(),InputRequired()])    
    password = PasswordField('Password',validators=[DataRequired(),InputRequired()])

class EditProfileForm(FlaskForm):
    username = TextField('Username',validators=[DataRequired(),InputRequired()])
    firstname = TextField('First Name',validators=[DataRequired(),InputRequired()])
    lastname = TextField('Last Name',validators=[DataRequired(),InputRequired()])
    photo = FileField('Add Profile Picture ',validators=[FileAllowed(['jpg','jpeg','png'],'Images Only!')])
    dob = TextField('Date of Birth',validators=[DataRequired()])
    gender = SelectField('Gender',choices=[('M','Male'),('F','Female'),('Other','Other')],validators=[DataRequired()])
    telephone = TextField('Mobile Number',validators=[DataRequired(),InputRequired()])
    email = TextField('Email Address',validators=[DataRequired(),Email()])
    password = PasswordField('Password')


class LoginForm(FlaskForm):
    username = TextField('',validators=[DataRequired(),InputRequired()])
    password = PasswordField('',validators=[InputRequired()])


class PostForm(FlaskForm):
    description = TextAreaField('Write your Post here',validators=[DataRequired()])
    
    
class PhotoForm(FlaskForm):
    caption = TextAreaField('Write your Post here',validators=[DataRequired()])
    photo = FileField('',validators=[FileAllowed(['jpg','jpeg','png'],'Images Only!')])

class GroupForm(FlaskForm):
    groupName = TextField("Group Name",validators=[InputRequired()])
    description = TextField("Pick a description that best suits your group")