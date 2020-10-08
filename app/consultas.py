from configuraciones import *
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

conn = psycopg2.connect(database=database, user=user, password=passwd, host=host)
cur = conn.cursor()

def datos_usuario(email):
	sql ="""
	SELECT correo,id_tipo,contrasena,id
	FROM usuario
	WHERE correo ='""" + email +"';"
	cur.execute(sql)
	results = cur.fetchone()
	return results

def obtener_tipo(id):
	sql ="""
	SELECT correo,id_tipo,contrasena,id
	FROM usuario
	WHERE id = """ + str(id) +";"
	cur.execute(sql)
	results = cur.fetchone()
	return results
#### Archivos de Consultas a la base SQL ####
"""
	SELECT relacion_ofe_atri.valor,atributo, ofertas.id,cupos, ofertas.fecha_creacion ,id_tipo, tipo_ofertas.tipo,estado.nombre, usuarios.id,relacion_usu_atri.valor
    FROM relacion_ofe_atri, ofertas, atributos_ofertas,tipo_ofertas,estado , usuarios, relacion_usu_atri
    WHERE ofertas.id = relacion_ofe_atri.id_ofe
    AND relacion_ofe_atri.id_atri = atributos_ofertas.id
    AND id_estado = estado.id
    AND id_tipo = tipo_ofertas.id
    AND usuarios.id = ofertas.id_usu_profe
    AND relacion_usu_atri.id_usu = ofertas.id_usu_profe
    AND (relacion_usu_atri.id_atri = '1' OR relacion_usu_atri.id_atri = '2' OR relacion_usu_atri.id_atri = '3')
    ORDER BY ofertas.id,relacion_usu_atri.valor ;


	SELECT usuarios.id, usuarios.email, array_to_string(array_agg(relacion_usu_atri.valor ORDER BY relacion_usu_atri.id_atri), ' ')
	FROM relacion_usu_atri , usuarios
	WHERE relacion_usu_atri.id_usu = usuarios.id
	AND(relacion_usu_atri.id_atri = '1' OR relacion_usu_atri.id_atri = '2' OR relacion_usu_atri.id_atri = '3')
	GROUP BY usuarios.id;
	;

	SELECT usuarios.id,valor, relacion_usu_atri.id_atri
	FROM relacion_usu_atri , usuarios
	WHERE relacion_usu_atri.id_usu = usuarios.id
	AND(relacion_usu_atri.id_atri = '1' OR relacion_usu_atri.id_atri = '2' OR relacion_usu_atri.id_atri = '3')
	GROUP BY usuarios.id,valor,relacion_usu_atri.id_atri
	ORDER BY usuarios.id,relacion_usu_atri.id_atri;
"""
