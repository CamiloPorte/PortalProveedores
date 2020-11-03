from configuraciones import *
import psycopg2

conn = psycopg2.connect(database=database, user=user, password=passwd, host=host)
cur = conn.cursor()

#### Codigo para limpiar la base de datos y setear con la configuración bajo el primer comando SQL ####

sql ="""DROP SCHEMA public CASCADE;
 CREATE SCHEMA public;"""
cur.execute(sql)

sql="""
CREATE TABLE tipos
  (id serial PRIMARY KEY,
  nombre varchar(255)
   );
"""
cur.execute(sql)

sql="""
CREATE TABLE proveedores
  (id serial PRIMARY KEY,
  nombre varchar(50),
  descripcion varchar(255)
   );
"""
cur.execute(sql)

sql="""
CREATE TABLE productos
  (codigo varchar(20) PRIMARY KEY,
  descripcion varchar(255)
   );
"""
cur.execute(sql)

sql="""
CREATE TABLE usuario
  (id serial PRIMARY KEY,
   id_tipo int,
   correo varchar(100),
   contrasena varchar(255),
   nombre varchar(50),
   apellido1 varchar(50),
   apellido2 varchar(50),
   FOREIGN KEY (id_tipo) REFERENCES tipos(id)
  );
"""
cur.execute(sql)


sql="""
CREATE TABLE pedido
 (id serial PRIMARY KEY ,
 id_usu integer,
 id_prov integer,
 n_orden decimal,
 descripcion varchar(255),
 fecha_arribo date,
 FOREIGN KEY (id_usu) REFERENCES usuario (id),
 FOREIGN KEY (id_prov) REFERENCES proveedores(id) 
);
"""
cur.execute(sql)

sql="""
CREATE TABLE prod_pedido
 (id_ped integer,
 codigo varchar(20),
 cant integer,
 PRIMARY KEY (id_ped, codigo, cant),
 FOREIGN KEY (id_ped) REFERENCES pedido (id),
 FOREIGN KEY (codigo) REFERENCES productos (codigo)
);
"""



cur.execute(sql)
conn.commit()
cur.close()
conn.close()
