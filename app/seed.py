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
INSERT INTO proveedores (nombre, descripcion, estado)
VALUES('Ok Nantong','Barras HWM, Accesorios, Maquinas ProMachine',True)
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion, estado)
VALUES('ByT Quindao','Bumper Plate HWM',True)
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion, estado)
VALUES('FIT Haiku','Mancuernas, Disco olimpicos y Barras',True)
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion, estado)
VALUES('AVIC','Cardio Obelix',True)
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion, estado)
VALUES('FAPRE','Piso de Caucho',True)
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion, estado)
VALUES('Nantong Kilyn','Maquinas Promachine y Ket Vinilo',True)
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion, estado)
VALUES('JADE','AIRBIKE',True)
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion, estado)
VALUES('SHANXHI','Cardio MediaGama',True)
;
"""
cur.execute(sql)

sql="""
INSERT INTO proveedores (nombre, descripcion, estado)
VALUES('ZHAOYANG','Máquinas de hogar',True)
;
"""
cur.execute(sql)

#######################################################


############ usuarios #########################

password = generate_password_hash("felipeporte123",method = "sha256")
sql="""
INSERT INTO usuario (id_tipo ,correo ,contrasena ,nombre ,apellido1 ,apellido2,estado )
VALUES(1, 'felipe.porte@pesaschile.cl','%s','Felipe','Porte','Moraga',True)
;
"""%(password)
cur.execute(sql)

password = generate_password_hash("jorgevilches123",method = "sha256")
sql="""
INSERT INTO usuario (id_tipo ,correo ,contrasena ,nombre ,apellido1 ,apellido2,estado )
VALUES(1, 'jorge.vilches@pesaschile.cl','%s','Jorge','Vilches','Valladares',True)
;
"""%(password)
cur.execute(sql)

password = generate_password_hash("12345",method = "sha256")
sql="""
INSERT INTO usuario (id_tipo ,correo ,contrasena ,nombre ,apellido1 ,apellido2,estado )
VALUES(2, 'camilo.porte@mail.udp.cl','%s','Camilo','Porte','Moraga',True)
;
"""%(password)
cur.execute(sql)

password = generate_password_hash("12345",method = "sha256")
sql="""
INSERT INTO usuario (id_tipo ,correo ,contrasena ,nombre ,apellido1 ,apellido2,estado )
VALUES(1, 'camilo.porte@pesaschile.cl','%s','Camilo','Porte','Moraga',True)
;
"""%(password)
cur.execute(sql)

##################################################





conn.commit()
cur.close()
conn.close()
