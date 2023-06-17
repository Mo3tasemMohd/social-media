

from flask import render_template, redirect, url_for, flash, request
from FlaskApp import app
from FlaskApp.forms import *
from .models import *
from FlaskApp import bcrypt
from flask_login import current_user, login_user, logout_user, login_required
from flask_migrate import Migrate

@app.route('/', methods=['GET', 'POST'])
@app.route('/Home', methods=['GET', 'POST'])
def home():
    
    form = PostForm()

    data = {
        'title': 'Flask Home',
        'navItem1': 'Home',
        'navItem2': 'About',
        'cssName': 'css/Home.css',
        'form': form
    }

    if current_user and current_user.is_authenticated:
        with app.app_context():
            posts = Post.query.all()
            data['posts'] = posts
    

    if form.validate_on_submit():
        with app.app_context():
            post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id, privacy=form.privacy.data)
            db.session.add(post)
            db.session.commit()
        flash(f"new post was added","success")
        return redirect(url_for('home'))
    

    with app.app_context():
        users = User.query.all()
        data['users'] = users


    return render_template('home.html', data=data)


@app.route('/About')
def about():
    data = {
        'title': "Flask About",
        'navItem1': 'Home',
        'navItem2': 'About',
        'cssName': 'css/About.css'
    }
    return render_template('about.html', data=data)




@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    data = {'form': form}
    if form.validate_on_submit():

    
        with app.app_context():
            hashpw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            print(hashpw)
            user = User(username=form.email.data.split('@')[0], email=form.email.data, password=hashpw)
            db.session.add(user)
            db.session.commit()
        flash(f"Registration Successful for {form.email.data.split('@')[0]}!","success")
        return redirect(url_for('login'))
    


    return render_template('register.html', data=data)



@app.route('/login', methods=['GET', 'POST'])
def login():


    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))


    form = LoginForm()
    data = {"form": form}
    with app.app_context():
        database = User.query.all()

    if form.validate_on_submit():
        for rec in database:
            
            if rec.email.lower() == form.email.data.lower() and bcrypt.check_password_hash(rec.password, form.password.data):
                with app.app_context():
                    user = User.query.filter_by(email=form.email.data).first()
                login_user(user)
                flash(f"Login Successful for {form.email.data.split('@')[0]}!","success")
                return redirect(url_for('home'))
            
        flash(f"Check your data!","danger")
        return redirect(url_for('login'))

    return render_template('login.html', data=data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ------------------- USER ENDPOINTS -------------------
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    data = {}
    with app.app_context():
        user = User.query.get(current_user.id)
 
    form = RegistrationForm(obj=user)

    data = {
        'id': id,
        'form': form,
    }
    
    
    if form.validate_on_submit():
        with app.app_context():
            user = User.query.get(current_user.id)
            user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
        return redirect(url_for('home'))

    return render_template('profile.html', data=data)



@app.route('/add_friend/<int:user_id>/<int:friend_id>', methods=['POST'])
def add_friend(user_id, friend_id):

    with app.app_context():
        exists = Friendship.query.filter(Friendship.user_id==user_id, Friendship.friend_id==friend_id).first()
        if exists:
            flash(f"User Exists as Friend!","danger")
        else:
            friendship = Friendship(user_id=user_id, friend_id=friend_id)
            db.session.add(friendship)
            db.session.commit()
            flash(f"User Added!","success")

    return redirect(url_for('home'))

@app.route('/remove_friend/<int:user_id>/<int:friend_id>', methods=['post'])
def remove_friend(user_id, friend_id):

    with app.app_context():
        friendship = Friendship.query.filter_by(user_id=user_id, friend_id=friend_id).first()
        db.session.delete(friendship)
        db.session.commit()
    return redirect(url_for('friends'))


  


@app.route('/friends', methods=['get'])
def friends():


    data = {}

    with app.app_context():
        list = db.session.query(
            User,
            Friendship
        )\
        .join(Friendship, Friendship.friend_id == User.id)\
        .filter(User.id == current_user.id)\
        .all()
        # list = Friendship.query.filter_by(user_id=current_user.id).all()
        print(list)
        data['users'] = list
    
    return render_template('friends.html', data=data)


# ------------------------- Post ENDPOINTS -----------

@app.route('/addPost',  methods=['GET', 'POST'])
# @login_required
def addPost():

    form = PostForm()

    data = {"form": form}


    if form.validate_on_submit():
      
        with app.app_context():
            post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id, privacy=form.privacy.data)
            db.session.add(post)
            db.session.commit()
        flash(f"new post was added","success")
        print('posts ', post)
        return redirect(url_for('home'))

    return render_template('newPost.html', data=data)


@app.route('/myPosts',  methods=['GET', 'POST'])
# @login_required
def myPosts(id=None):

    data = {}
  
    if current_user and current_user.is_authenticated:
        with app.app_context():
            posts = Post.query.filter_by(user_id = current_user.id)
            data['posts'] = posts
    


    
    return render_template('myPosts.html', data=data)




@app.route('/deletePost/<int:id>',  methods=['GET', 'Delete'])
@login_required
def deletePost(id):

    with app.app_context():
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()

    return redirect(url_for('myPosts'))


@app.route('/editPost/<int:id>',  methods=['GET', 'POST'])
@login_required
def editPost(id):

    with app.app_context():
        post = Post.query.get(id)
 
    form = PostForm(obj=post)

    data = {
        'id': id,
        'form': form,
    }
    
    
    if form.validate_on_submit():
        with app.app_context():
            post = Post.query.get(id)
            for key, value in form.data.items():
                if key == 'submit' or key == 'csrf_token':
                    continue
                setattr(post, key, value)      
            db.session.commit()
        return redirect(url_for('myPosts'))
        
            

    return render_template('editPost.html', data=data)