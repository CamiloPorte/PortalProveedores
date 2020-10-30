from configuraciones import *
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

conn = psycopg2.connect(database=database, user=user, password=passwd, host=host)
cur = conn.cursor()

############ tipos #################
sql="""
INSERT INTO tipos (nombre)
VALUES('Administrador')
;
"""
cur.execute(sql)

sql="""
INSERT INTO tipos (nombre)
VALUES('Vendedor')
;
"""
cur.execute(sql)

###################################################
conn.commit()

######### proveedores ######################
sql="""
INSERT INTO proveedores (nombre, descripcion)
VALUES('Ok Nantong','Barras HWM, Accesorios, Maquinas ProMachine')
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion)
VALUES('ByT Quindao','Bumper Plate HWM')
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion)
VALUES('FIT Haiku','Mancuernas, Disco olimpicos y Barras')
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion)
VALUES('AVIC','Cardio Obelix')
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion)
VALUES('FAPRE','Piso de Caucho')
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion)
VALUES('Nantong Kilyn','Maquinas Promachine y Ket Vinilo')
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion)
VALUES('JADE','AIRBIKE')
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion)
VALUES('SHANXHI','Cardio MediaGama')
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion)
VALUES('ZHAOYANG','Máquinas de hogar')
;
"""
cur.execute(sql)

#######################################################


############ usuarios #########################

password = generate_password_hash("felipeporte123",method = "sha256")
sql="""
INSERT INTO usuario (id_tipo ,correo ,contrasena ,nombre ,apellido1 ,apellido2 )
VALUES(1, 'felipe.porte@pesaschile.cl','%s','Felipe','Porte','Moraga')
;
"""%(password)
cur.execute(sql)

password = generate_password_hash("jorgevilches123",method = "sha256")
sql="""
INSERT INTO usuario (id_tipo ,correo ,contrasena ,nombre ,apellido1 ,apellido2 )
VALUES(1, 'jorge.vilches@pesaschile.cl','%s','Jorge','Vilches','Valladares')
;
"""%(password)
cur.execute(sql)

password = generate_password_hash("12345",method = "sha256")
sql="""
INSERT INTO usuario (id_tipo ,correo ,contrasena ,nombre ,apellido1 ,apellido2 )
VALUES(2, 'camilo.porte@mail.udp.cl','%s','Camilo','Porte','Moraga')
;
"""%(password)
cur.execute(sql)

password = generate_password_hash("12345",method = "sha256")
sql="""
INSERT INTO usuario (id_tipo ,correo ,contrasena ,nombre ,apellido1 ,apellido2 )
VALUES(1, 'camilo.porte@pesaschile.cl','%s','Camilo','Porte','Moraga')
;
"""%(password)
cur.execute(sql)

##################################################





conn.commit()
cur.close()
conn.close()
