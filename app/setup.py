from configuraciones import *
import psycopg2

conn = psycopg2.connect(database=database, user=user, password=passwd, host=host)
cur = conn.cursor()

#### Código para limpiar la base de datos y setear con la configuración bajo el primer comando SQL ####

sql ="""DROP SCHEMA public CASCADE;
 CREATE SCHEMA public;"""
cur.execute(sql)

#sql="""
#CREATE TABLE atributos_usuario
#  (id serial PRIMARY KEY,
#   atributo varchar(255)
#   );
#"""
#cur.execute(sql)


#sql="""
#CREATE TABLE tipo_usuario
#  (id serial PRIMARY KEY,
#   tipo varchar(255)
#  );
#"""
#cur.execute(sql)



#sql="""
#CREATE TABLE usuarios
# (id serial PRIMARY KEY,
#  tipo integer,
#  email varchar(50),
#  password varchar (255),
#  rut varchar(11),
#  fecha_creacion date,
#  FOREIGN KEY (tipo) REFERENCES tipo_usuario(id)
# );
#"""
#cur.execute(sql)


#sql="""
#CREATE TABLE relacion_usu_atri
# (id_usu integer,
# id_atri integer,
# valor varchar(255),
# PRIMARY KEY (id_usu, id_atri, valor),
# FOREIGN KEY (id_usu) REFERENCES usuarios (id),
# FOREIGN KEY (id_atri) REFERENCES atributos_usuario(id) 
#);
#"""
cur.execute(sql)
conn.commit()
cur.close()
conn.close()
