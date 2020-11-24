import os
import re
from datetime import datetime

from flask import abort, flash, redirect, render_template, request, session, url_for
from flask.json import jsonify
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from app import app, db, login_manager
from app.forms import EditProfileForm, GroupForm, LoginForm, PhotoForm, PostForm, RegisterForm
from app.models import *


# home route
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    postform = PostForm()
    photoform = PhotoForm()
    posts = []
    friends = []
    groups = []
    comments = []
    photo_comments = []

    friends_result = db.session.execute("""SELECT user.* ,login.username FROM login,user WHERE login.user_id=user.user_id
        AND login.user_id IN
        (SELECT user.user_id FROM user JOIN friends ON user.user_id=friends.friend_id JOIN login ON friends.user_id=login.user_id WHERE login.username=BINARY(:username));""",
                                        {"username": current_user.username})
    for row in friends_result:
        row = dict(row)
        friends.append(row)

    group_result = db.session.execute("""SELECT * FROM `group`;""")
    for row in group_result:
        row = dict(row)
        groups.append(row)

    if request.method == 'POST' and postform.validate_on_submit():
        description = postform.description.data
        db.session.execute("""INSERT INTO post(user_id,description) VALUES(:user_id,:description)""",
                           {"user_id": current_user.user_id, "description": description})
        db.session.commit()
        flash("Post added Successfully.", "success")
        return redirect(url_for('home'))

    elif request.method == "POST" and photoform.validate_on_submit():
        caption = photoform.caption.data
        photo = photoform.photo.data
        if (photo):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(
                app.config['UPLOAD_FOLDER']+'/posts', filename))
            db.session.execute("""INSERT INTO photos(user_id,caption,filename) VALUES(:user_id,:caption,:filename)""",
                               {"user_id": current_user.user_id, "caption": caption, "filename": filename})
            db.session.commit()
            flash("Post added Successfully.", "success")
            return redirect(url_for('home'))
    else:
        post_result = db.session.execute(
            """SELECT post.* FROM post ORDER BY post.post_id DESC LIMIT 5 """)
        posts = [row for row in post_result]
        comment_result = db.session.execute(
            """SELECT post.post_id,post.description, comments.comment,login.username FROM post JOIN comments ON post.post_id=comments.post_id JOIN login ON comments.user_id=login.user_id""")
        for row in comment_result:
            row = dict(row)
            comments.append(row)
        photo_result = db.session.execute(
            """SELECT * FROM photos ORDER BY photo_id DESC""")
        photos = [row for row in photo_result]

        photo_comment_result = db.session.execute(
            """SELECT photos.photo_id, photos.caption,photo_comments.comment, login.username FROM photos JOIN photo_comments ON photos.photo_id=photo_comments.photo_id JOIN login ON photo_comments.user_id = login.user_id """)
        for row in photo_comment_result:
            row = dict(row)
            photo_comments.append(row)
        db.session.close()
        return render_template('home.html', postform=postform, photoform=photoform, posts=posts, photos=photos, friends=friends, groups=groups, comments=comments, photo_comments=photo_comments)


# login page
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        result = db.session.execute(
            """CALL GetCredentials(:username)""", {"username": username})
        if(result.rowcount):
            for i in result:
                user_id = i[0]
                username = i[1]
                hash_pw = i[2]
            user = Login(user_id, username, password)
            if user is not None and check_password_hash(hash_pw, user.password):
                password = None
                login_user(user)
                db.session.execute("""UPDATE login SET login_date=CURDATE() WHERE user_id IN (SELECT user_id FROM user WHERE user_id=:user_id)""",
                                   {"user_id": current_user.user_id})
                db.session.commit()
                flash("Logged in successfully!", "success")
                return redirect(url_for('home'))
                db.session.close()
            else:
                flash('Username or Password is incorrect.', 'danger')
    form_errors(form)
    return render_template("login.html", form=form)


# route to admin interface
@app.route('/admin', methods=["POST", "GET"])
@login_required
def adminui():
    allusers = []
    allposts = []
    allgroups = []

    allusers_result = db.session.execute(
        """SELECT user.*,login.username FROM user JOIN login WHERE user.user_id=login.user_id LIMIT 10""")
    for row in allusers_result:
        row = dict(row)
        allusers.append(row)

    allpost_results = db.session.execute("""SELECT * FROM post LIMIT 10 """)
    for row in allpost_results:
        row = dict(row)
        allposts.append(row)

    allgroups_result = db.session.execute(
        """SELECT * FROM `group` LIMIT 10 """)
    for row in allgroups_result:
        row = dict(row)
        allgroups.append(row)

    return render_template("admin.html", allusers=allusers, allposts=allposts, allgroups=allgroups)


# group route
# this route specifies which group you wanna go to
@app.route('/group/<int:group_id>', methods=['GET', 'POST'])
# for now i'll remove the group_name part
def group(group_id):
    # this looks into the templates folder and finds the corresponding file and loads it.
    group = {}
    group_members = []
    friends = []
    group_result = db.session.execute("""SELECT * FROM `group` WHERE group_id=:group_id""",
                                      {"group_id": group_id})
    for row in group_result:
        group = dict(row)
    group_members_result = db.session.execute(
        """SELECT login.username ,group_members.role,`group`.* FROM login JOIN group_members ON login.user_id = group_members.user_id JOIN `group` ON group_members.group_id=`group`.`group_id` WHERE `group`.`group_id`=:group_id""",
        {"group_id": group_id})
    for row in group_members_result:
        row = dict(row)
        group_members.append(row)

    friends_result = db.session.execute("""SELECT user.* ,login.username, profile.filename FROM login,user,profile WHERE login.user_id=user.user_id
        AND profile.user_id=user.user_id AND login.user_id IN
        (SELECT user.user_id FROM user JOIN friends ON user.user_id=friends.friend_id JOIN login ON friends.user_id=login.user_id WHERE login.username=BINARY(:username));""",
                                        {"username": current_user.username})
    for row in friends_result:
        row = dict(row)
        friends.append(row)
    return render_template("group.html", group=group, group_members=group_members, friends=friends)


# Profile of user

@app.route('/u/<string:username>')
@login_required
def profile(username):
    friends = []
    profile = {}
    profile_pic = ""
    friend_profile_pic = []
    groups = []

# Get list of users from database
    friends_result = db.session.execute("""SELECT user.* ,login.username, profile.filename FROM login,user,profile WHERE login.user_id=user.user_id
        AND profile.user_id=user.user_id AND login.user_id IN
        (SELECT user.user_id FROM user JOIN friends ON user.user_id=friends.friend_id JOIN login ON friends.user_id=login.user_id WHERE login.username=BINARY(:username));""",
                                        {"username": username})
    for row in friends_result:
        row = dict(row)
        friends.append(row)
# Get profile information from database
    profile_result = db.session.execute("""SELECT login.username,user.* FROM user JOIN login ON user.user_id=login.user_id WHERE login.username=BINARY(:username)""",
                                        {"username": username})
    for row in profile_result:
        profile = dict(row)

# Get profile picture of user from database
    profile_pic_result = db.session.execute("""SELECT filename FROM profile WHERE user_id IN (SELECT user_id from login where username=BINARY(:username))""",
                                            {"username": username})

# Checks if query returned a result if not set profile picture to default
    if profile_pic_result.rowcount == 0:
        profile_pic = get_image(None)
    else:
        for rows in profile_pic_result:
            profile_pic = get_image(rows[0])
# Gets group that user is apart of
    group_result = db.session.execute("""SELECT * FROM `group` where group_id IN (SELECT group_id FROM group_members WHERE user_id=:user_id )""",
                                      {"user_id": current_user.user_id})
    for row in group_result:
        row = dict(row)
        groups.append(row)

# Renders user specific profile
    if (current_user.username == username):
        return render_template('profile.html', friends=friends, profile=profile, profile_pic=profile_pic, groups=groups)
    else:
        if(profile):
            return render_template("profile.html", friends=friends, profile_pic=profile_pic, profile=profile)
        else:
            abort(404)


# edit user profile route
@app.route("/edit/profile/<string:user_id>", methods=["POST", "GET"])
@login_required
def edit_profile(user_id):
    form = EditProfileForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        dob = form.dob.data
        gender = form.gender.data
        email = form.email.data
        password = form.password.data
        telephone = re.sub(r'[^\w]', '', form.telephone.data)
        photo = form.photo.data

        if (photo):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.session.execute("""UPDATE profile SET filename=:filename WHERE user_id=:user_id""",
                               {"filename": filename, "user_id": user_id})
            db.session.commit()
        else:
            db.session.execute("""UPDATE user SET first_name=:first_name, last_name=:last_name,email_address=:email,dob=:dob,gender=:gender,telephone=:phone WHERE user_id=:user_id """,
                               {"first_name": firstname, "last_name": lastname, "email": email, "dob": dob, "gender": gender, "phone": telephone, "user_id": current_user.user_id})
            db.session.commit()

            db.session.execute("""UPDATE login SET username=:username WHERE user_id=:user_id""",
                               {"username": username, "user_id": current_user.user_id})
            db.session.commit()
            if(password):
                db.session.execute("""UPDATE login SET password=:password WHERE user_id=:user_id""",
                                   {"password": generate_password_hash(password), "user_id": current_user.user_id})
                db.session.commit()
        flash("Profile Updated Successfully", "success")
        return redirect(url_for("profile", username=username))
    else:
        result = db.session.execute("""SELECT first_name,last_name,email_address,telephone,dob,gender FROM user WHERE user_id=:user_id""",
                                    {"user_id": current_user.user_id})

        credentials = {}

        for row in result:
            credentials = dict(row)

        return render_template("edit_profile.html", form=form, credentials=credentials)


# register user route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        password = form.password.data
        email = form.email.data
        dob = form.dob.data
        gender = form.gender.data
        profile_pic = form.photo.data
        filename = secure_filename(profile_pic.filename)
        profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        created_on = datetime.today().strftime('%Y-%m-%d')
        phone = re.sub(r'[^\w]', '', form.telephone.data)
        db.session.execute("""INSERT INTO user(first_name,last_name,email_address,telephone,dob,gender) VALUES(:firstname,:lastname,:email,:phone,:dob,:gender)""",
                           {"firstname": firstname, "lastname": lastname, "email": email, "phone": phone, "dob": dob, "gender": gender})
        db.session.commit()
        db.session.execute("""INSERT INTO login(username,password,login_date) VALUES(:username,:password,CURDATE());""",
                           {"username": username, "password": generate_password_hash(password, method='pbkdf2:sha512')})
        db.session.commit()
        db.session.execute("""UPDATE profile SET filename=:filename WHERE user_id IN (SELECT user_id FROM user WHERE email_address=:email)""",
                           {"filename": filename, "email": email})
        db.session.commit()

        flash('Profile successfully added, Welcome %s' % username, 'success')
        return redirect(url_for('login'))

    form_errors(form)
    return render_template('register.html', form=form)


# create group route
@app.route("/create/group", methods=['POST', 'GET'])
def create_group():
    form = GroupForm()

    if request.method == 'POST' and form.validate_on_submit():
        groupName = form.groupName.data
        description = form.description.data

        if description:
            db.session.execute("""INSERT INTO `group`(group_name,description) VALUES(:group_name,:description)""",
                               {"group_name": groupName, "description": description})
            db.session.commit()
        else:
            db.session.execute("""INSERT INTO `group`(group_name) VALUES(:group_name)""",
                               {"group_name": groupName})
            db.session.commit()
        db.session.execute("""INSERT INTO group_members VALUES(:user_id,(SELECT group_id FROM `group` WHERE group_name=:group_name),:role)""",
                           {"user_id": current_user.user_id, "group_name": groupName, "role": 'admin'})
        db.session.commit()
        flash('Group successfully created, You are the Administrator of  %s' %
              groupName, "success")
        return redirect(url_for('login'))

    form_errors(form)
    return render_template('create_group.html', form=form)


# logout user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'warning')
    return redirect(url_for('login'))


# api routes go here
@app.route("/api/add/group", methods=['POST'])
def add_user():
    content = request.json
    user_id = content['group_btn']
    group_id = content['group_id']
    if request.method == "POST":
        db.session.execute("""INSERT INTO group_members(user_id,group_id,role) VALUES(:user_id,:group_id,:role)""",
                           {"user_id": user_id, "group_id": group_id, "role": 'content editor'})
        db.session.commit()
        message = "Friend Added To Group Successfully"
        data = [{"message": message}]
        return jsonify(data=data)
    else:
        return ("error")


@app.route("/api/comment",methods=['POST'])
def comment():
    if request.method == "POST":
        content = request.json
        post_id = content['comment_btn']
        comment = content['comment']
        db.session.execute("""INSERT INTO comments VALUES(:user_id,:post_id,:comment) """,
        {"user_id":current_user.user_id,"post_id":post_id,"comment":comment})
        db.session.commit()
    return "Successful"


@app.route("/api/add", methods=['POST'])
def add_friend():
    if request.method == "POST":
        content = request.json
        db.session.execute("""INSERT INTO friends VALUES(:user_id,:friend_id)""",
                           {"user_id": current_user.get_id(), "friend_id": content})
        db.session.commit()
        message = "Friend Added Successfully"
        data = [{"message": message}]
        return jsonify(data=data)
    else:
        return ("error")


@app.route("/api/comment/photo", methods=['POST'])
def photo_comment():
    if request.method == 'POST':
        content = request.json
        comment = content['comment']
        photo_id = content['comment_btn']
        print(content)
        db.session.execute("""INSERT INTO photo_comments VALUES(:user_id,:photo_id,:comment)""",
        {"user_id":current_user.user_id,"photo_id":photo_id,"comment":comment})
        db.session.commit()
        return "Successful"


###
# The functions below should be applicable to all Flask apps.
###

@login_manager.user_loader
def load_user(user_id):
    return check_user(user_id)


def get_image(filename):
    rootdir = os.getcwd()
    for subfir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
        if filename in files:
            return filename
        else:
            filename = 'default.jpg'
            return filename


def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)

    return error_messages


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
