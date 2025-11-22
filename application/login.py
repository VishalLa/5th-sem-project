from flask import (
    Flask, 
    render_template, 
    request,
    redirect, 
    url_for, 
    session,
    Blueprint
)
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps
from .model import User
from .database import db
import uuid
import re

login_controller = Blueprint('login_controller', __name__)

@login_controller.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.find_by_email(email)
        if user and user.check_password(password):
            session['user'] = email
            return redirect(url_for('home'))
        else:
            error = "Invalid credentials"
    return render_template('login.html', error=error)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login_controller.login'))
        return f(*args, **kwargs)
    return decorated_function


@login_controller.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_controller.login'))


# Signup route
@login_controller.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # Basic validations
        if not name or not email or not password or not confirm:
            error = 'All fields are required.'
            return render_template('signup.html', error=error)

        if password != confirm:
            error = 'Passwords do not match.'
            return render_template('signup.html', error=error)

        if len(password) < 6:
            error = 'Password must be at least 6 characters.'
            return render_template('signup.html', error=error)

        # simple email format check
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            error = 'Invalid email address.'
            return render_template('signup.html', error=error)

        # check existing user
        existing = User.find_by_email(email)
        if existing:
            error = 'Email already registered.'
            return render_template('signup.html', error=error)

        # create user id
        user_id = uuid.uuid4().hex[:8]

        # create user
        try:
            user = User.create_user(user_id, name, email, password)
        except Exception as e:
            db.session.rollback()
            error = f'Error creating user: {str(e)}'
            return render_template('signup.html', error=error)

        # auto-login
        session['user'] = email
        return redirect(url_for('home'))

    return render_template('signup.html', error=None)
