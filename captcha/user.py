
import requests
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app

from captcha.database import get_db

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.before_app_request
def load_logged_in_user():
    # check whether the request is more than 3 for a given ip address
    cache = current_app.cache

    # get client ip
    client_ip = str(request.environ["REMOTE_ADDR"])
    client_ip_hits = cache.get(client_ip)
    if client_ip_hits and int(client_ip_hits) > 3:
        g.show_recaptcha = True
    else:
        g.show_recaptcha = False


@bp.route("/register", methods=("GET", "POST"))
def register():
    # Register a new user and validate the email
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # validate captche before db hit
        verified_flag = None
        recaptcha_response = request.form.get(current_app.config["RECAPTCHA_RESPONSE_PARAM"])
        if recaptcha_response:
            verified_flag = validate_recaptcha_response(recaptcha_response)
            if not verified_flag:
                clear_flash()
                flash("Recaptcha verification failed, try again")
                return redirect(url_for("user.register"))

        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not email:
            error = "Email is required"
        elif not password:
            error = "Password is required."
        else:
            user_id = db.users.find_one({"email": email})
            if user_id is not None:
                error = "User {0} is already registered.".format(username)

        if error is None:
            # user is not registered, store in the mongodb
            user_details = {
                "username": username,
                "email": email,
                "password": password
            }
            db.users.insert_one(user_details).inserted_id
            update_request_count()
            clear_flash()
            success_message = "Registration Successful"
            if verified_flag:
                success_message += " with verified captcha"
            flash(success_message)
            return redirect(url_for("user.register"))

        clear_flash()
        flash(error)

    return render_template("register.html")


def clear_flash():
    # clear the flash message
    session.pop("_flashes", None)


def update_request_count():
    # If the client exist, update the count otherwise insert the client
    cache = current_app.cache

    # get client ip
    client_ip = str(request.environ["REMOTE_ADDR"])
    client_ip_hits = cache.get(client_ip)
    if not client_ip_hits:
        cache.set(client_ip, 1)
    else:
        cache.set(client_ip, int(client_ip_hits)+1)


def validate_recaptcha_response(token):
    # validate the recaptcha from the google server
    resp = requests.post(url=current_app.config["SITE_VERIFY_URL"],
                         data={"secret": current_app.config["SITE_SECRET"], "response": token})
    if resp.json().get("success"):
        return True
    return False
