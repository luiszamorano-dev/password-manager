from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import TextAreaField

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')]
    )
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PasswordForm(FlaskForm):
    site = StringField('Sitio/Servicio', validators=[DataRequired()])
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Guardar')

class SetPinForm(FlaskForm):
    pin = PasswordField('PIN' , validators=[DataRequired(), Length(min=4, max=10)])
    confirm_pin = PasswordField('confirmar PIN' , validators=[
        DataRequired(),
        EqualTo('pin' , message='Los PINs deben coincidir.')
    ])
    submit = SubmitField('Guardar PIN')

class VerifyPinForm(FlaskForm):
    pin = PasswordField('PIN', validators=[DataRequired()])
    submit = SubmitField('Verificar')