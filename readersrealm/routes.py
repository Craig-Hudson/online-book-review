from flask import render_template, request, redirect, url_for
from readersrealm import app, db
# from readersrealm.models import


@app.route("/")
def home():
    return render_template("base.html")
