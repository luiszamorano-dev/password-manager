from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Password

routes = Blueprint('routes', __name__)

@routes.route('/')
@login_required  # Solo usuarios logueados pueden acceder
def index():
    # Obtener las contraseñas del usuario actual
    passwords = Password.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', passwords=passwords)