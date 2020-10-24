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

class BuscarPedidoForm(FlaskForm):
    codigo = StringField('Código', validators=[Length(min=2, max=50)])
    nombre = StringField('Nombre de producto', validators=[Length(min=2, max=50)])


class loginForm(FlaskForm):
    email = StringField('Correo electronico', validators=[Email(), DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=2, max=50)])
    def validate(self):
        results = datos_usuario(self.email.data)
        if not FlaskForm.validate(self):
            return False
        if results == None or not check_password_hash(results[2],self.password.data):
            self.email.errors.append('Usuario inexistente o contraseña errada')
            self.password.errors.append('Usuario inexistente o contraseña errada')
            return False
        return True
        
class ingresarPedidoForm(FlaskForm):
    proveedores = obtener_proveedores()
    numero_de_orden=IntegerField('Numero De Orden', validators=[DataRequired(), Length(min=1, max=50)])
    descripcion=StringField('Descripción', validators=[DataRequired(), Length(min=2, max=255)])
    fecha_de_arribo=DateField('Fecha De Arribo', format="'%d/%m/%Y'",validators=[DataRequired()])
    proveedor=SelectField('Proveedor', choices=[(tipo[0],tipo[1])for tipo in proveedores] ,validators=[DataRequired()])


class crearUsuariosForm(FlaskForm):
    tipos=obtener_tipos()
    email = StringField('Correo electronico', validators=[Email(), DataRequired(), Length(min=2, max=50)])
    confirmacio_email=StringField('Confirmación correo electronico', validators=[Email(), DataRequired(), Length(min=2, max=50)])
    password = PasswordField( 'Contraseña', validators=[DataRequired(), Length(min=2, max=50)] )
    nombre_usuario = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellido1_usuario = StringField('Apellido Paterno', validators=[DataRequired(), Length(min=2, max=50)])
    apellido2_usuario = StringField('Apellido Materno', validators=[DataRequired(), Length(min=2, max=50)])
    tipo_cuenta=SelectField('Tipo de cuenta', coerce=int,choices=[(tipo[0],tipo[1])for tipo in tipos] ,validators=[DataRequired()])
    def validate(self):
        results = datos_usuario(self.email.data)
        if not FlaskForm.validate(self):
            return False
        if self.confirmacio_email.data != self.email.data or results != None:
            if self.confirmacio_email.data != self.email.data:
                self.email.errors.append('Los correos electrónicos deben coincidir')
                self.confirmacio_email.errors.append('Los correos electrónicos deben coincidir')
            if results != None:
                self.email.errors.append('Usuario ya existente')
                self.confirmacio_email.errors.append('Usuario ya existente')
            return False
        return True

class crearProveedorForm(FlaskForm):
    nombre_proveedor = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    descripcion=StringField('Descripción', validators=[DataRequired(), Length(min=2, max=255)])

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if existe_proveedor(self.nombre_proveedor.data):
            self.nombre_proveedor.errors.append('Proveedor ya existente')
            return False
        return True
