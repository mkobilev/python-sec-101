from time import time

from flask_login import login_required
from models import Product
from server import db

from flask import Blueprint, redirect, render_template, url_for

website = Blueprint("website", __name__)


@website.route("/")
@login_required
def index():
    return render_template(
        "index.html", products=db.session.execute(db.select(Product)).scalars().all()
    )


@website.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="img/favicon.svg"))
