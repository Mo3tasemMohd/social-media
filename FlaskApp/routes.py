

from flask import render_template, redirect, url_for, flash
from FlaskApp import app
from FlaskApp.forms import RegistrationForm, LoginForm
from .models import *
from FlaskApp import bcrypt
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/Home')
def home():
    data = {
        'title': 'Flask Home',
        'navItem1': 'Home',
        'navItem2': 'About',
        'cssName': 'css/Home.css'

    }
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
@app.route('/profile')
@login_required
def profile():
    return "profile"

@app.route('/friends')
@login_required
def friends():
    return "friends"