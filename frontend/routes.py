import os
import secrets
from PIL import Image 
from flask import render_template, url_for, flash, redirect, request, abort
from frontend import app, db, bcrypt
from frontend.forms import registrationForm, loginForm, PostForm
from frontend.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from senClassifier import pred

@app.route("/")
#Call home page from here and pass all the post from the database in assending order
@app.route("/home")
@login_required
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=3)
    return render_template("home.html",posts=posts)

#Register page is called here pass the register form and verify if data is proper and add to database
@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = registrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email = form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

#Login page is called here and check if the user is already loged in or not 
#if the user is not loged in load the login page and verify the credential from database
@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Wrong Email or password",'danger')
    return render_template('login.html',title='Login',form=form)

#Louout the user
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#Post new post from the logged in user at that time and check if the post contains any bad words
@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        c = form.content.data
        if pred(c)==1:
            flash('Post contains inappropriate content and can not be posted','danger')
            return redirect(url_for('home'))
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post has been created','success')
        return redirect(url_for('home'))
    return render_template('create_post.html',title='New Post', form = form, legend = "New Post")

#Display seperate post for viewing purpose 
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)

#Display all the post from a specific user when clicked on the user name 
@app.route("/user/<string:username>")
@login_required
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=3)
    return render_template("user_posts.html",posts=posts,user=user)
