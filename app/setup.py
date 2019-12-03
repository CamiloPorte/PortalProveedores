from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))

cur = conn.cursor()
sql ="""DROP SCHEMA public CASCADE;
 CREATE SCHEMA public;"""

cur.execute(sql)
sql="""
CREATE TABLE mesas
           (numero serial PRIMARY KEY,
            zona_fumadores boolean,
            capacidad integer
            );
"""
cur.execute(sql)
sql="""
CREATE TABLE empleados
           (nombre varchar(255),
           apellido varchar(255),
           rut varchar(10) PRIMARY KEY NOT NULL,
           password varchar (255),
           admin boolean
           );
"""
cur.execute(sql)
sql="""
CREATE TABLE productos
           (id_producto serial PRIMARY KEY,
            cantidad integer,
            valor integer ,
            nombre varchar(255)
            );
"""
cur.execute(sql)
sql="""
CREATE TABLE proveedores
           (nombre varchar (255),
           rut_empresa varchar(10) PRIMARY KEY,
           idproducto integer,
           cant_mercaderia integer,
           FOREIGN KEY (idproducto) REFERENCES productos (id_producto)
           );
"""
cur.execute(sql)
sql="""
CREATE TABLE menus
           (id_menu varchar(255) PRIMARY KEY,
           precio_menu integer,
           descuento integer
           );
"""
cur.execute(sql)
sql="""
CREATE TABLE pedidos
			(cant_atendida integer,
			fecha varchar(40),
            hora varchar(40),
			rut_empleado varchar(10),
			num_mesa integer,
			idmenu varchar(255),
			PRIMARY KEY( cant_atendida,fecha,hora,rut_empleado,num_mesa,idmenu),
			FOREIGN KEY (rut_empleado) REFERENCES empleados(rut),
			FOREIGN KEY (num_mesa) REFERENCES mesas (numero)
			);
"""
cur.execute(sql)

sql="""
CREATE TABLE reservas
			(id_mesa integer,
			fecha varchar(110),
            hora varchar(40),
            FOREIGN key( id_mesa) REFERENCES mesas(numero),
			PRIMARY KEY( id_mesa,fecha,hora)
			);
"""
cur.execute(sql)

sql="""
CREATE TABLE llevan
			(producto integer,
            menu varchar(150),
            FOREIGN key (producto) REFERENCES productos(id_producto),
            FOREIGN key (menu) REFERENCES menus(id_menu),
			PRIMARY KEY( producto ,menu)
			);
"""
cur.execute(sql)

sql="""
CREATE TABLE traen
			(producto integer,
            cantidad integer,
            fecha varchar(150),
            FOREIGN key (producto) REFERENCES productos(id_producto),
            FOREIGN key (menu) REFERENCES menus(id_menu),
			PRIMARY KEY( producto ,menu)
			);
"""
cur.execute(sql)
conn.commit()
cur.close()
conn.close()
