
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from captcha.database import get_db

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.before_app_request
def load_logged_in_user():
    # check whether the request is more than 3 for a given ip address
    client_ip = request.environ['REMOTE_ADDR']
    print ("========update the google captche=========")
    if hasattr(g, 'client_IPs'):
        total_request = g.client_IPs.get(client_ip)

        if total_request > 3:
            pass
            # introduce the capche
    else:
        g.client_IPs = dict()
        


@bp.route('/register', methods=('GET', 'POST'))
def register():
    # Register a new user and validate the email
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required'
        elif not password:
            error = 'Password is required.'
        else:
            user_id = db.users.find_one({"email": email})
            if user_id is not None:
                error = 'User {0} is already registered.'.format(username)

        if error is None:
            # user is not registered, store in the mongodb
            user_details = {
                'username': username,
                'email': email,
                'password': password
            }
            db.users.insert_one(user_details).inserted_id
            update_request_count()
            clear_flash()
            flash("Register Successful")
            return redirect(url_for('user.register'))

        clear_flash()
        flash(error)

    return render_template('register.html')


def clear_flash():
    # clear the flash message
    session.pop('_flashes', None)


def update_request_count():
    # If the client exist, update the count otherwise insert the client
    client_ip = request.environ['REMOTE_ADDR']
    client_exist = g.client_IPs.get(client_ip)

    if not client_exist:
        g.client_IPs[client_ip] = 1
    else:
        g.client_IPs[client_ip] += 1