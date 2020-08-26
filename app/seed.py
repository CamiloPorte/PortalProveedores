from configuraciones import *
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

conn = psycopg2.connect(database=database, user=user, password=passwd, host=host)
cur = conn.cursor()

############tipos de usuarios#################
sql="""
INSERT INTO tipo_usuario (tipo)
VALUES('Admin')
;
"""
cur.execute(sql)

sql="""
INSERT INTO tipo_usuario (tipo)
VALUES('Profesor')
;
"""
cur.execute(sql)

sql="""
INSERT INTO tipo_usuario (tipo)
VALUES('Alumno')
;
"""
cur.execute(sql)
###################################################
conn.commit()

#########atributos de usuarios######################
sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('Nombre completo')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('Apellido paterno')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('Apellido materno')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('RUT')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('Nacionalidad')
;
"""
cur.execute(sql)

sql="""

INSERT INTO atributos_usuario (atributo)
VALUES('Direccion')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('Telefono')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('Carrera')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('Año de ingreso')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('Promedio acumulado')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('Ayudantía(s)')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('Taller(es) de perfeccionamiento')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('Actividades extracurriculares')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_usuario (atributo)
VALUES('Publicaciones universitarias')
;
"""
cur.execute(sql)

#1 nombre_completo
#2 apellido_paterno
#3 apellido_materno
#4 direccion
#######################################################


############ usuarios admin #########################
password = generate_password_hash("12345",method = "sha256")
sql="""
INSERT INTO usuarios (tipo ,email ,password ,rut ,fecha_creacion )
VALUES(1, 'camilo.porte@mail.udp.cl','%s','12345678-1',current_timestamp)
;
"""%(password)
cur.execute(sql)

password2 = generate_password_hash("12345",method = "sha256")
sql="""
INSERT INTO usuarios (tipo ,email ,password ,rut ,fecha_creacion )
VALUES(1, 'jorge.floresl@mail.udp.cl','%s','12345678-2',current_timestamp)
;
"""%(password2)
cur.execute(sql)

password3 = generate_password_hash("123456",method = "sha256")
sql="""
INSERT INTO usuarios (tipo ,email ,password ,rut ,fecha_creacion )
VALUES(1, 'cristian.maira@mail.udp.cl','%s','12345678-3',current_timestamp)
;
"""%(password3)
cur.execute(sql)

sql="""
INSERT INTO relacion_usu_atri (id_usu ,id_atri ,valor )
VALUES(1,1,'Camilo')
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_usu_atri (id_usu ,id_atri ,valor )
VALUES(1,2,'Porte')
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_usu_atri (id_usu ,id_atri ,valor )
VALUES(2,1,'Jorge')
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_usu_atri (id_usu ,id_atri ,valor )
VALUES(2,2,'Flores')
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_usu_atri (id_usu ,id_atri ,valor )
VALUES(3,1,'Cristian')
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_usu_atri (id_usu ,id_atri ,valor )
VALUES(3,2,'maira')
;
"""
cur.execute(sql)

##################################################

##############tipos de ofertas####################
sql="""
INSERT INTO tipo_ofertas (tipo )
VALUES('Tesis')
;
"""
cur.execute(sql)

sql="""
INSERT INTO tipo_ofertas (tipo )
VALUES('Memoria')
;
"""
cur.execute(sql)
 
sql="""
INSERT INTO tipo_ofertas (tipo )
VALUES('Práctica electiva')
;
"""
cur.execute(sql)

sql="""
INSERT INTO tipo_ofertas (tipo )
VALUES('Ayudantía de investigación')
;
"""
cur.execute(sql)

sql="""
INSERT INTO tipo_ofertas (tipo )
VALUES('Personal técnico de apoyo a proyecto')
;
"""
cur.execute(sql)

sql="""
INSERT INTO tipo_ofertas (tipo )
VALUES('Proyecto/trabajo de asignatura')
;
"""
cur.execute(sql)

conn.commit()

#1 tesis
#2 memoria
#3 practica electiva
#4 ayudantia de investigacion
#5 personal tecnico
#6 proyecto o trabajo de clases
##############################################

########### estado #############

sql="""
INSERT INTO Estado (nombre)
VALUES('Terminado')
;
"""
cur.execute(sql)

sql="""
INSERT INTO Estado (nombre)
VALUES('En proceso')
;
"""
cur.execute(sql)

sql="""
INSERT INTO Estado (nombre)
VALUES('En espera')
;
"""
cur.execute(sql)

sql="""
INSERT INTO Estado (nombre)
VALUES('Aceptado')
;
"""
cur.execute(sql)

sql="""
INSERT INTO Estado (nombre)
VALUES('No aceptado')
;
"""
cur.execute(sql)

###########################################

########### atributos ofertas ###############
sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Nombre del proyecto')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Nombre del proyecto asociado')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('URL')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Horas por semana')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Semanas a trabajar')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Descripción')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Remuneración')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Requisitos')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Correo electronico de contacto')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Telefono de contacto')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Fecha cierre de postulaciones')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Fecha de entrega de resultados')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Nombre tesis')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Fecha de publicación')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Nombre del cargo')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Proyectos de investigación asociados')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Nombre del profesor')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Cupos')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Fecha de inicio')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Fecha de término')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Fecha de cierre de recepción de antecedentes')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Nombre de la asignatura')
;
"""
cur.execute(sql)

sql="""
INSERT INTO atributos_ofertas (atributo)
VALUES('Sigla de la asignatura')
;
"""
cur.execute(sql)

#1 nombre del proyecto asociado
#2 url
#3 hrs por semana
#4 semanas a trabajar
#5 descripcion
#6 remuneracion
#7 requisitos
#8 email contacto
#9 fono contacto
#10 fecha cierre postulaciones
#11 fecha entrega resultados
#12 carta de postulacion
#13 nombre tesis
#14 fecha publicacion
#15 nombre del cargo
#16 proyectos de investigacion asociados
#17 n de horas por semana
#18 nombre profesor
#19 cupos
#20 fecha de inicio
#21 fecha de termino
#22 fecha de cierre de recepcion de antecedentes
#23 nombre de la asgnatura
#24 sigla asignatura

############################################

############## relacion tipo oferta atributos #########

########## atributos para tesis o memoria ##############

sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 1)
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 3)
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 4)
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 5)
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 19)
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 20)
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 6)
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 7)
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 8)
;
"""
cur.execute(sql)


sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 9)
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 10)
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 21)
;
"""
cur.execute(sql)

sql="""
INSERT INTO relacion_ofe_tipo_atri (id_tipo, id_atri)
VALUES(1, 12)
;
"""
cur.execute(sql)


########## ayudantia de investigacion ##############



conn.commit()
cur.close()
conn.close()
