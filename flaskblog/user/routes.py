from flask import (Blueprint,redirect,flash,url_for,render_template,request)
from flask_login import login_required,current_user,login_user,logout_user

from flaskblog import db,bcrypt
from flaskblog.models import Post,User

from flaskblog.user.forms import (LoginForm,RegistrationForm,Request_ResetForm,Pswd_ResetForm,Updateinfo)
from flaskblog.user.utils import save_img,send_reset_email

users= Blueprint('users',__name__)

@users.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login Unsuccessful, please check your Email and Password',category='danger')
    return render_template('login.html',title='Login',form=form)

@users.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,password=hashed_pw,email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created For {form.username.data}! You can now Log in',category='success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='Register',form=form)

@users.route("/logout")
def logout():
   logout_user()
   return redirect(url_for('main.home'))


@users.route("/account",methods=['GET','POST'])
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
        return redirect(url_for('main.account')) #prevents resubmission of form {prompt window}
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file =url_for('static',filename='profile pics/'+current_user.image_file)
    return render_template('account.html',title='Account',profile_image=image_file,form=form)


@users.route("/user/<string:username>")
def user_page(username):
    page = request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=3,page=page)
    return render_template('user_posts.html',user=user,posts=posts,title='User')


@users.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Request_ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email is been sent with Instructions!', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password Request', form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    print(f"Token received: {token}")
    user = User.verify_reset_token(token)
    print(f"User from token: {user}")
    if user is None:
        flash('This is a Invalid or Expired Token', 'warning')
        return redirect(url_for('users.reset_password'))
    form = Pswd_ResetForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw  # No need to find or add since we did that up also we only need to update.
        db.session.commit()
        flash(f'Password Updated For {user.username}! You can now Log in', category='success')
        return redirect(url_for('users.login'))
    return render_template('change_password.html', title='Reset Password', form=form)