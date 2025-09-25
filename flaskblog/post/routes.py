from flask import (Blueprint,redirect,flash,url_for,render_template,abort,request)
from flask_login import login_required,current_user
from flaskblog import db
from flaskblog.models import Post
from flaskblog.post.forms import PostForm

posts= Blueprint('posts',__name__)

@posts.route("/post/create",methods=["GET","POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user) #can use user_id instead of the backref
        db.session.add(post)
        db.session.commit()

        flash('Your Post has been uploaded!',category='success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html',title='new post',
                           legend='Create Post',form=form)

@posts.route("/post/<int:post_id>",methods=["GET","POST"])
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)


@posts.route("/post/<int:post_id>/update",methods=["GET","POST"])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash(f'Your Post has been updated!','success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method =='GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html',title='Update Post',
                           legend='Update Post',form=form)

@posts.route("/post/<int:post_id>/delete",methods=["POST"])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your Post has been deleted!', 'dark')
    return redirect(url_for('main.home'))
