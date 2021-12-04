from operator import pos
from flask import Flask, Blueprint, flash, redirect, url_for
from flask.globals import request
from flask.templating import render_template
from flask_login import login_required, current_user
from . import db
from .models import Comment, Post, User, Like 

views = Blueprint("views", __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', user = current_user, posts = posts)

@views.route('/create-post', methods = ['GET' , 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            flash('Post cant not be empty', category='error')
        else:
            post = Post(text = text, author = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post successfully created!', category='success')
 
    return render_template('create_post.html', user = current_user)

@views.route('/delete-post/<id>')
@login_required 
def delete_post(id):

    post = Post.query.filter_by(id=id).first()
    if not post:
        flash('Post does not exist.', category = 'error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post', category = 'error')
    else : 
        db.session.delete(post)
        db.session.commit()
    
    return redirect(url_for('views.home'))

@views.route('/posts/<username>')
@login_required
def posts(username):

    # user - > who's posts are being viewed, username is of this guy
    # current_user -> who's trying to view user's posts

    user = User.query.filter_by(username = username).first()
    if not user:
        flash('User does exist', catergory = 'error')
        return redirect(url_for('views.home'))

    posts = user.posts

    return render_template('posts.html', user = current_user, posts=posts, username = username)


@views.route('/create-comment/<post_id>', methods = ['POST'])
@login_required
def create_comment(post_id):

    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty', category = 'error')
    else :
        post = Post.query.filter_by(id = post_id)
        if post : 
            flash('Comment created', category='success')
            comment = Comment(text = text, author = current_user.id, post_id = post_id)
            db.session.add(comment)
            db.session.commit()
        else :
            flash('Post does not exist', category='error')

    return redirect(url_for('views.home'))

@views.route('/delete-comment/<id>')
@login_required 
def delete_comment(id):
    comment = Comment.query.filter_by(id = id).first()
    if not comment:
        flash('Comment does not exist', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted', category='success')

    return redirect(url_for('views.home'))

@views.route('like-post/<post_id>', methods = ['GET'])
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id = post_id)
    like = Like.query.filter_by(author = current_user.id, post_id = post_id)
    if not post:
        flash('Post does not exist', category='error')
    elif like :
        db.session.delete(like)
        db.session.commit()
    else:
        db.session.add(like)
        db.session.commit()


    return redirect(url_for('views.home'))

