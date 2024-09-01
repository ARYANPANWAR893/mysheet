from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import *
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                login_user(user, remember=True)
                return redirect(url_for('routes.home'))
            else:
                return redirect(url_for('auth.signup'))
        else:
            return redirect(url_for('auth.signup'))

    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if len(password)<8:
            return redirect("/signup?err=1")

        new_user = User(name=name, username=username,
                        email=email, password=password, email_v=0)
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(email=email).first()
        login_user(user, remember=True)
        return redirect(url_for('routes.home'))
    
    msg = request.args.get("err")
    if msg ==str(1):
        msg = "Password must contain atleast 8 characters."

    return render_template('signup.html', msg=msg)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))