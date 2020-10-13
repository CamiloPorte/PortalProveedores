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

def obtener_pedidos():
	sql ="""
	SELECT nombre,pedido.descripcion,proveedores
	FROM pedido,proveedores
	WHERE id_prov = proveedores.id
	; 
	"""
	cur.execute(sql)
	results = cur.fetchall()
	return results

def obtener_pedidos_filtrados(codigo,nombre):
	sql ="""
	SELECT nombre,pedido.descripcion,proveedores
	FROM pedido,proveedores
	WHERE id_prov = proveedores.id
	; 
	"""
	cur.execute(sql)
	results = cur.fetchall()
	return results

def obtener_proveedores():
	sql ="""
	SELECT id,nombre
	FROM proveedores
	;
	"""
	cur.execute(sql)
	results = cur.fetchall()
	return results

def obtener_tipos():
	sql ="""
	SELECT id,nombre
	FROM tipos
	;
	"""
	cur.execute(sql)
	results = cur.fetchall()
	return results

def existe_producto(codigo):
	sql ="""
	SELECT *
	FROM productos
	WHERE codigo ='""" + codigo +"';" 

	cur.execute(sql)
	results = cur.fetchall()
	return results

def crear_producto(codigo,descripcion):
	sql="""
	INSERT INTO productos (codigo, descripcion)
	VALUES('%s','%s')
	;
	"""%(codigo, descripcion) 
	cur.execute(sql)
	conn.commit()

def insertar_producto(id_ped,codigo,descripcion):
	sql="""
	INSERT INTO prod_pedido (id_ped, codigo,cant)
	VALUES(%s,'%s',%s)
	;
	"""%(id_ped,codigo, descripcion) 
	cur.execute(sql)
	conn.commit()

def crear_pedido(id_usu, id_prov, n_orden,descripcion , fecha_arribo, excel):
	sql="""
	INSERT INTO pedido (id_usu, id_prov,n_orden, descripcion , fecha_arribo)
	VALUES(%s,%s,%s,'%s','%s')
	RETURNING id
	;
	"""%(id_usu, id_prov,n_orden, descripcion , fecha_arribo)
	cur.execute(sql)
	conn.commit()
	id_ped = cur.fetchone()
	filas, columnas= excel.shape
	for i in range(filas):
		existe = existe_producto(excel[i][1])
		if len(existe) == 0:
			crear_producto(excel[i][1],excel[i][2])
		insertar_producto(id_ped[0],excel[i][1],excel[i][4])
		print("codigo: ",excel[i][1],"|","descripcion: ",excel[i][2],"|","cantidad: ",excel[i][4])
	


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
