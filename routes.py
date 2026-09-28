from flask import flash, redirect, render_template, request, url_for , session
from app import app
from models import db ,  User 
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

@app.route('/')
def index():
    #user_id in session to check if user is logged in
    if 'user_id' in session:
        return render_template('index.html')
    else:
        flash('You need to log in first.')
        return redirect(url_for('login'))
        

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.passhash, password):
        flash('Invalid username or password.')
        return redirect(url_for('login'))

    session['user_id'] = user.id
    flash('You have successfully logged in.')

    return redirect(url_for('index'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/layout')
def layout():
    return render_template('layout.html')


@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    confirm_password = request.form.get('confirm_password')

    if not username or not password or not email or not confirm_password:
       flash('Please fill in all fields.')
       return redirect(url_for('register'))

    if password != confirm_password:
        flash('Passwords do not match.')
        return redirect(url_for('register'))

    
    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists.')
        return redirect(url_for('register'))

    password = generate_password_hash(password)

    new_user = User(username=username, passhash=password, name=email)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))

def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id'  in session:
           return func(*args, **kwargs)
        else: 
            flash('please log in first.') 
            return redirect(url_for('login'))            
    return inner


@app.route('/profile')
@auth_required
def profile():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('profile.html', user=user)
    else:
        flash('You need to log in first.')
        return redirect(url_for('login'))

@app.route('/profile', methods=['POST'])
@auth_required
def update_profile():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        username = request.form.get('username')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')

        if username:
            user.username = username
        if password:
            if not check_password_hash(user.passhash, cpassword):
                flash('Current password is incorrect.')
                return redirect(url_for('profile'))
            user.passhash = generate_password_hash(password)

        db.session.commit()
        flash('Profile updated successfully.')
        return redirect(url_for('profile'))
    else:
        flash('You need to log in first.')
        return redirect(url_for('login'))

    if username != user.username:
        new_username = User.query.filter_by(username=username).first()
        if new_username:
            flash('Username already exists.')
            return redirect(url_for('profile'))

    new_username = request.form.get('username')
    user.username = new_username
    user.passhash = generate_password_hash(request.form.get('password'))
    user.name = name
    db.session
    flash('Profile updated successfully.')
    return redirect(url_for('profile'))

@app.route('/logout')
@auth_required
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))