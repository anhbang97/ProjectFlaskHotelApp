from flask import render_template, redirect
from PackageApp import app, login
from flask_login import login_user
from PackageApp.admin import *

import hashlib


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/room-standard")
def room_standard():
    return render_template("room-standard.html")


@app.route("/room-deluxe")
def room_deluxe():
    return render_template("room-deluxe.html")


@app.route("/room-superior")
def room_superior():
    return render_template("room-superior.html")


@app.route("/room-suite")
def room_suite():
    return render_template("room-suite.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/room")
def room():
    return render_template("room.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/blog-single")
def blog_single():
    return render_template("blog-single.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/login-client")
def login_from_client():
    return render_template("loginCL.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login-admin", methods=["GET", "POST"])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.user_name == username.strip(),
                                 User.user_password == password).first()

        if user:
            login_user(user=user)
    return redirect("/admin")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=False)