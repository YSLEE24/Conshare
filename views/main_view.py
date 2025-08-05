from flask import Blueprint
from flask import render_template
from flask_login import current_user

main_bp = Blueprint('main', __name__, url_prefix="/")

@main_bp.route("/", methods=['GET'])
def index():
    return render_template('index.html')