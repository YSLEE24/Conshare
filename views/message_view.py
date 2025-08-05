# message_view.py

from flask import Blueprint, render_template

message_bp = Blueprint('message', __name__, template_folder='templates')

@message_bp.route("/contactbox")
def contactbox():
    return render_template("contactbox.html")