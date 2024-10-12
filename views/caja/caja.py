from flask import Blueprint, request, render_template
from extensions import db

caja_bp = Blueprint('caja', __name__)

@caja_bp.route('/caja')
def caja():
    return render_template('caja.html')