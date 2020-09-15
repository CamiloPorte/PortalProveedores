from configuraciones import *
import psycopg2
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateTimeField, HiddenField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError, InputRequired
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
# login 
class loginForm(FlaskForm):
    email = StringField('Correo electronico', validators=[Email(), DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=2, max=50)])
    tipo = SelectField('Tipo de cuenta',choices=[("2","Vendedor"),("1","Administrador")] ,validators=[DataRequired()])
'''
    def validate(self):
        results = datos_usuario(self.email.data, self.tipo.data)
        if not FlaskForm.validate(self):
            return False
        if results == None or not check_password_hash(results[2],self.password.data):
            self.email.errors.append('Usuario inexistente o contraseña errada')
            self.tipo.errors.append('Usuario inexistente o contraseña errada')
            self.password.errors.append('Usuario inexistente o contraseña errada')
            return False
        return True'''
        
class ingresarPedido(FlaskForm):
    proveedor=SelectField('Proveedor',choices=[("1","chinito1"),("2","chinito2")] ,validators=[InputRequired()])
    numero_de_orden=IntegerField('Numero De Orden', validators=[DataRequired(), Length(min=1, max=50)])
    descripcion=StringField('Descripción', validators=[DataRequired(), Length(min=2, max=255)])
    fecha_de_arribo=DateField('Fecha De Arribo', format="'%d/%m/%Y'",Validators=[DataRequired()])


class crearUsuarios(FlaskForm):
    email = StringField('Correo electronico', validators=[Email(), DataRequired(), Length(min=2, max=50)])
    password = PasswordField( 'Contraseña', validators=[DataRequired(), Length(min=2, max=50)] )
    nombre_usuario = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])

class crearProveedor(FlaskForm):
    nombre_proveedor = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    descripcion=StringField('Descripción', validators=[DataRequired(), Length(min=2, max=255)])

class crearProveedores(FlaskForm):
    nombre_proveedor = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    descripcion=StringField('Descripción', validators=[DataRequired(), Length(min=2, max=255)])
