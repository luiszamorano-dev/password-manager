from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import Password, db, User
from app.forms import PasswordForm, SetPinForm, VerifyPinForm
from app.crypto import encrypt_password, decrypt_password
from app import db
from flask import session, redirect, url_for, flash, request, render_template
from datetime import datetime, timedelta


routes = Blueprint('routes', __name__)

def pin_validated():
    last_verified = session.get('pin_verified_at')
    if not last_verified:
        return False
    last_verified = datetime.fromisoformat(last_verified)
    if datetime.utcnow() - last_verified > timedelta(minutes=5): # Tiempo de sesión válido
        session.pop('pin_verified_at')
        return False
    return True

@routes.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PasswordForm()
    if form.validate_on_submit():
        encrypted_pw = encrypt_password(form.password.data)
        new_password = Password(
            site=form.site.data,
            username=form.username.data,
            password_encrypted=encrypted_pw,
            user_id=current_user.id
        )
        db.session.add(new_password)
        db.session.commit()
        flash('Contraseña guardada correctamente.', 'success')
        return redirect(url_for('routes.index'))

    passwords = Password.query.filter_by(user_id=current_user.id).all()
    for p in passwords:
        p.password_decrypted = decrypt_password(p.password_encrypted)

    return render_template('index.html', passwords=passwords, form=form)

@routes.route('/configurar_pin', methods=['GET', 'POST'])
@login_required
def configurar_pin():
    form = SetPinForm()
    if form.validate_on_submit():
        current_user.set_pin(form.pin.data)
        db.session.commit()
        flash('PIN guardado exitosamente.')
        return redirect(url_for('routes.index'))
    return render_template('configurar_pin.html', form=form)

@routes.route('/ser-pin', methods=['GET', 'POST'])
@login_required
def set_pin():
    form = SetPinForm()
    if form.validate_on_submit():
        current_user.set_pin(form.pin.data)
        db.session.commit()
        flash('PIN guardado correctamente')
        return redirect(url_for('routes.dashboard')) # O cualquier pagina principal
    return render_template('set_pin.html', form=form)

@routes.route('/verify_pin/<int:site_id>', methods=['GET', 'POST'])
@login_required
def verify_pin(site_id):
    form = VerifyPinForm()
    if form.validate_on_submit():
        if current_user.check_pin(form.pin.data):
            session['pin_verified_at'] = datetime.utcnow().isoformat()
            return redirect(url_for('routes.view_site_passwords', site_id=site_id))
        else:
            flash("PIN incorrecto", "danger")
    return render_template('verify_pin.html', form=form)

@routes.route('/site/<int:site_id>')
@login_required
def view_site_passwords(site_id):
    if not pin_validated():
        return redirect(url_for('routes.verify_pin', site_id=site_id))

    entries = Password.query.filter_by(user_id=current_user.id, site=site_id).all()
    return render_template('view_passwords.html', entries=entries)