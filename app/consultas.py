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
	SELECT n_orden,nombre,proveedores.descripcion,pedido.descripcion, to_char(fecha_arribo,'DD-MM-YYYY'),pedido.id
	FROM pedido,proveedores
	WHERE id_prov = proveedores.id
	ORDER BY fecha_arribo
	; 
	"""
	cur.execute(sql)
	results = cur.fetchall()
	return results

def obtener_pedidos_filtrados(codigo,nombre):
	sql ="""
	SELECT n_orden,nombre,proveedores.descripcion,pedido.descripcion, to_char(fecha_arribo,'DD-MM-YYYY'),pedido.id,cant
	FROM pedido,proveedores, prod_pedido,productos
	WHERE id_prov = proveedores.id
	AND prod_pedido.codigo = producto.codigo
	AND prod_pedido.id_ped = pedido.id
	AND productos.codigo = "%s"
	; 
	"""%(codigo.upper())
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

def existe_proveedor(nombre):
	sql ="""
	SELECT id,nombre
	FROM proveedores
	WHERE nombre = "%s"
	;
	"""%(nombre)
	cur.execute(sql)
	results = cur.fetchall()
	if results != None:
		return True
	return False

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
	WHERE codigo ='""" + codigo.upper() +"';" 

	cur.execute(sql)
	results = cur.fetchall()
	return results

def crear_producto(codigo,descripcion):
	sql="""
	INSERT INTO productos (codigo, descripcion)
	VALUES('%s','%s')
	;
	"""%(codigo.upper(), descripcion) 
	cur.execute(sql)
	conn.commit()

def insertar_producto(id_ped,codigo,descripcion):
	sql="""
	INSERT INTO prod_pedido (id_ped, codigo,cant)
	VALUES(%s,'%s',%s)
	;
	"""%(id_ped,codigo.upper(), descripcion) 
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

def crear_proveedor(nombre,descripcion):
	sql="""
	INSERT INTO proveedores (nombre, descripcion)
	VALUES('%s','%s')
	;
	"""%(nombre,descripcion) 
	cur.execute(sql)
	conn.commit()

def crear_usuarios(email,password,nombre_usuario,apellido1_usuario,apellido2_usuario,tipo_cuenta):
	contrasena = generate_password_hash(password,method = "sha256")
	sql="""
	INSERT INTO usuario (id_tipo,correo,contrasena,nombre,apellido1,apellido2)
	VALUES(%s,'%s','%s','%s','%s','%s')
	;
	"""%(tipo_cuenta,email,contrasena,nombre_usuario,apellido1_usuario,apellido2_usuario)
	cur.execute(sql)
	conn.commit()

def obtener_productos_pedido(id):
	sql ="""
	SELECT productos.codigo, productos.descripcion, cant
	FROM productos, prod_pedido, pedido
	WHERE pedido.id = prod_pedido.id_ped
	AND prod_pedido.codigo = productos.codigo
	AND pedido.id = %s
	;
	"""%(str(id))
	cur.execute(sql)
	results = cur.fetchall()
	return results


#### Archivos de Consultas a la base SQL ####
