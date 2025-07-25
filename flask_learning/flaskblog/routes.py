import os
import secrets
from PIL import Image
from flask import render_template,url_for,flash,redirect,request
from flaskblog import app,bcrypt,db,login_manager
from flask_login import login_user,logout_user,current_user,login_required
from flaskblog.models import User,Post
from flaskblog.forms import RegistrationForm, LoginForm,Updateinfo

posts = [
    {
        'author':'Dummy1',
        'title':'What can i do with this?',
        'content':'First content',
        'date':'April, 2025'
    },
    {
        'author':'Dummy2',
        'title':'What cant i do with this?',
        'content':'second content',
        'date':'April, 2026'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts,title='Home')

@app.route("/about")
def about():
    return render_template('about.html',title='About')

@app.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form =LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page= request.args.get('next') #args-> dict, hence better to accessed with get() then [k,v]; Will return None or a key 
            print(next_page) 
            flash(f'Login Successful! Welcome {user.username }',category='success') 
            # if the user accesses the account page through URL it will redirect it to the 'account' 
            # and if through normal login it will redirect it to the home page.
            return redirect(next_page) if next_page else redirect(url_for('home')) 
        else:
            flash(f'Login Unsuccessful, please check your Email and Password',category='danger')
    return render_template('login.html',title='Login',form=form)

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,password=hashed_pw,email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created For {form.username.data}! You can now Log in',category='success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route("/logout")
def logout():
   logout_user()
   return redirect(url_for('home'))

def save_img(form_img,old_img):
    random_hex=secrets.token_hex(8)
    _,img_ext=os.path.splitext(form_img.filename)
    image_fn=random_hex+img_ext
    image_path= os.path.join(app.root_path,'static/profile pics',image_fn)

    # Save Space!!!!
    image_size=(131,131)
    i =Image.open(form_img)
    i.thumbnail(image_size)
    i.save(image_path)

    # delete the previous img if the user uploades the new successfully exp->default.png
    if old_img != 'default.png':
        old_path=os.path.join(app.root_path,'static/profile pics',old_img)
        if os.path.exists(old_path):
            os.remove(old_path)

    return image_fn

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=Updateinfo()
    if form.validate_on_submit():
        if form.profile_img.data:
            old_img=current_user.image_file
            image_fn = save_img(form.profile_img.data,old_img)
            current_user.image_file = image_fn
        current_user.username=form.username.data
        current_user.email= form.email.data
        db.session.commit()
        flash(f'Your Account has been updated!',category='success')
        return redirect(url_for('account')) #prevents resubmission of form {prompt window}
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file =url_for('static',filename='profile pics/'+current_user.image_file)
    return render_template('account.html',title='Account',profile_image=image_file,form=form)

