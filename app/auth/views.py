from flask import flash, redirect, render_template, url_for, Flask, g, request
import flask_login
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms  import LoginForm, RegistrationForm
from .. import db
from ..models import Employee

from app import oidc

# reference: https://github.com/puiterwijk/flask-oidc.git

@auth.route('/login')
@oidc.require_login
def login():
    if oidc.user_loggedin:
        flash('Welcome!')
        return redirect(url_for('home.dashboard'))
    else:
        flash('Error, login failed')
        return redirect(url_for('home.homepage'))


# @auth.route('/private')
# @oidc.require_login
# def hello_me():
#     info = oidc.user_getinfo(['email', 'openid_id'])
#     return ('Hello, %s (%s)! <a href="/">Return</a>' %
#             (info.get('email'), info.get('openid_id')))


# @auth.route('/api')
# @oidc.accept_token(True, ['openid'])
# def hello_api():
#     return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})


@auth.route('/logout')
def logout():
    oidc.logout()
    if not oidc.user_loggedin:
        flash('Logout Successful')
    else:
        flash('Unknown error occured')

    return redirect(url_for('home.homepage'))

# @auth.route('/register', methods=['GET', 'POST'])
# def register():
#     """
#     Handle requests to the /register route
#     Add an employee to the database through the registration form
#     """
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         employee = Employee(email=form.email.data,
#                             username=form.username.data,
#                             first_name=form.first_name.data,
#                             last_name=form.last_name.data,
#                             password=form.password.data)

#         # add employee to the database
#         db.session.add(employee)
#         db.session.commit()
#         flash('You have successfully registered! You may now login.')

#         # redirect to the login page
#         return redirect(url_for('auth.login'))

#     # load registration template
#     return render_template('auth/register.html', form=form, title='Register')


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     """
#     Handle requests to the /login route
#     Log an employee in through the login form
#     """
#     form = LoginForm()
#     if form.validate_on_submit():

#         # check whether employee exists in the database and whether
#         # the password entered matches the password in the database
#         employee = Employee.query.filter_by(email=form.email.data).first()
#         if employee is not None and employee.verifypassword(
#                 form.password.data):
#             # log employee in
#             login_user(employee)

#             # redirect to the dashboard page after login
#             if employee.is_admin:
#                 return redirect(url_for('home.admin_dashboard'))
#             else:
#                 return redirect(url_for('home.dashboard'))


#         # when login details are incorrect
#         else:
#             flash('Invalid email or password.')

#     # load login template
#     return render_template('auth/login.html', form=form, title='Login')


# @auth.route('/logout')
# @login_required
# def logout():
#     """
#     Handle requests to the /logout route
#     Log an employee out through the logout link
#     """
#     logout_user()
#     flash('You have successfully been logged out.')

#     # redirect to the login page
#     return redirect(url_for('auth.login'))
