# views/admin_view.py

from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from ..models import Booking

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route("/bookings")
@login_required
def admin_bookings():
    if current_user.role == 'admin':
        bookings = Booking.query.all()
        return render_template("admin/bookings.html", bookings=bookings)
    else:
        abort(403)