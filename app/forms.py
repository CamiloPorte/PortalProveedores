from configuraciones import *
import psycopg2
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateTimeField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from consultas import *
conn = psycopg2.connect(database=database, user=user, password=passwd, host=host)
cur = conn.cursor()

#### Archivo de formularios de la librería wtforms ####

"""
class boton_postular(FlaskForm):
    oferta_id = HiddenField(validators=[DataRequired(), Length(min=2, max=50)])
    guardar = SubmitField('Postular')


class loginForm(FlaskForm):
    email = StringField('Correo electronico', validators=[Email(), DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=2, max=50)])
    tipo = SelectField('Tipo de cuenta',choices=[("1","Administrador"),("2","Profesor"),("3","Alumno")] ,validators=[DataRequired()])

    def validate(self):
        results = datos_usuario(self.email.data, self.tipo.data)
        if not FlaskForm.validate(self):
            return False
        if results == None or not check_password_hash(results[2],self.password.data):
            self.email.errors.append('Usuario inexistente o contraseña errada')
            self.tipo.errors.append('Usuario inexistente o contraseña errada')
            self.password.errors.append('Usuario inexistente o contraseña errada')
            return False
        return True

"""
