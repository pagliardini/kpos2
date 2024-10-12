from flask import Blueprint, request, render_template
from extensions import db

compras_bp = Blueprint('compras', __name__)

@compras_bp.route('/compras')
def compras():
    return render_template('compras.html')