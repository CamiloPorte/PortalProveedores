from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))

cur = conn.cursor()


sql="""
INSERT INTO mesas (zona_fumadores ,capacidad )
VALUES(True,2)
;
"""
cur.execute(sql)

sql="""
INSERT INTO mesas (zona_fumadores ,capacidad )
VALUES(True,3)
;
"""
cur.execute(sql)

sql="""
INSERT INTO mesas (zona_fumadores ,capacidad )
VALUES(True,2)
;
"""
cur.execute(sql)

sql="""
INSERT INTO mesas (zona_fumadores ,capacidad )
VALUES(True,4)
;
"""
cur.execute(sql)

sql="""
INSERT INTO mesas (zona_fumadores ,capacidad )
VALUES(True,2)
;
"""
cur.execute(sql)

sql="""
INSERT INTO mesas (zona_fumadores ,capacidad )
VALUES(false,2)
;
"""
cur.execute(sql)

sql="""
INSERT INTO mesas (zona_fumadores ,capacidad )
VALUES(false,2)
;
"""
cur.execute(sql)

sql="""
INSERT INTO mesas (zona_fumadores ,capacidad )
VALUES(false,5)
;
"""
cur.execute(sql)

sql="""
INSERT INTO mesas (zona_fumadores ,capacidad )
VALUES(false,5)
;
"""
cur.execute(sql)

sql="""
INSERT INTO mesas (zona_fumadores ,capacidad )
VALUES(false,3)
;
"""
sql="""
INSERT INTO empleados (nombre , apellido , rut, password , admin)
VALUES ('Camilo','Porte','19280181-8','123456',True);
"""
cur.execute(sql)

sql="""
INSERT INTO empleados (nombre , apellido , rut, password , admin)
VALUES ('Nombre','Falso1','12345678-5','123456',false);
"""
cur.execute(sql)

sql="""
INSERT INTO empleados (nombre , apellido , rut, password , admin)
VALUES ('Nombre','Falso2','12345678-8','123456',false);
"""
cur.execute(sql)

sql="""
INSERT INTO empleados (nombre , apellido , rut, password , admin)
VALUES ('Nombre','Falso3','12345678-9','123456',false);
"""
cur.execute(sql)

sql="""
INSERT INTO empleados (nombre , apellido , rut, password , admin)
VALUES ('Nombre','Falso4','12345678-1','123456',false);
"""
cur.execute(sql)

sql="""
INSERT INTO empleados (nombre , apellido , rut, password , admin)
VALUES ('Capitan','Sudamerica','12345678-2','123456',false);
"""
cur.execute(sql)

sql="""
INSERT INTO empleados (nombre , apellido , rut, password , admin)
VALUES ('Tito','Fernandez','12345678-3','123456',false);
"""
cur.execute(sql)

sql="""
INSERT INTO empleados (nombre , apellido , rut, password , admin)
VALUES ('Pretoriano','El Estratega','12345678-4','123456',false);
"""
cur.execute(sql)

sql ="""
INSERT INTO productos(cantidad, valor , nombre)
VALUES ('500','4000','Pepsi 3L');
"""
cur.execute(sql)

sql ="""
INSERT INTO productos(cantidad, valor , nombre)
VALUES ('500','4000','Coca Cola 3L');
"""
cur.execute(sql)

sql ="""
INSERT INTO productos(cantidad, valor , nombre)
VALUES ('500','6000','Pizza');
"""
cur.execute(sql)

sql ="""
INSERT INTO productos(cantidad, valor , nombre)
VALUES ('500','4500','Pimienta');
"""
cur.execute(sql)

sql ="""
 INSERT INTO proveedores (nombre,rut_empresa,cant_mercaderia,idproducto)
 VALUES ('Cokecompany','6006000','18','6');
"""

cur.execute(sql)

sql ="""
 INSERT INTO proveedores (nombre,rut_empresa,cant_mercaderia,idproducto)
 VALUES ('ccu','6006001','180','5');
"""
cur.execute(sql)

sql ="""
 INSERT INTO proveedores (nombre,rut_empresa,cant_mercaderia,idproducto)
 VALUES ('pjspa','6006002','182','7');
"""
cur.execute(sql)


sql ="""
 INSERT INTO proveedores (nombre,rut_empresa,cant_mercaderia,idproducto)
 VALUES ('saleros salsita','6006006','187888','8');
"""
cur.execute(sql)


sql ="""
 INSERT INTO menus (id_menu , precio_menu)
 VALUES ('colacion','15000');
"""
cur.execute(sql)

sql="""
 INSERT INTO llevan (producto ,menu) VALUES ('7','colacion')
"""
cur.execute(sql)

sql="""
 INSERT INTO llevan (producto ,menu) VALUES ('5','colacion')
"""
cur.execute(sql)

sql ="""
 INSERT INTO menus (id_menu , precio_menu)
 VALUES ('pepi','8000');
"""
cur.execute(sql)

sql="""
 INSERT INTO llevan (producto ,menu) VALUES ('5','pepi')
"""
cur.execute(sql)

sql ="""
 INSERT INTO menus (id_menu , precio_menu)
 VALUES ('picza','12000');
"""
cur.execute(sql)

sql="""
 INSERT INTO llevan (producto ,menu) VALUES ('7','picza')
"""
cur.execute(sql)

sql="""
INSERT INTO pedidos (cant_atendida , fecha, hora , rut_empleado , num_mesa ,
			idmenu ) VALUES ('3','10/9/2018' , '20:30','19280181-8','10','picza');
"""
cur.execute(sql)
sql="""
INSERT INTO pedidos (cant_atendida , fecha, hora , rut_empleado , num_mesa ,
			idmenu ) VALUES ('3','10/9/2018','20:30','19280181-8','10','pepi');
"""
cur.execute(sql)
sql="""
INSERT INTO pedidos (cant_atendida , fecha, hora , rut_empleado , num_mesa ,
			idmenu ) VALUES ('4','10/9/2018','22:30','12345678-9','11','picza');
"""
cur.execute(sql)
sql="""
INSERT INTO pedidos (cant_atendida , fecha, hora , rut_empleado , num_mesa ,
			idmenu ) VALUES ('5','10/9/2018','22:30','12345678-8','12','picza');
"""
cur.execute(sql)
sql="""
INSERT INTO pedidos (cant_atendida , fecha, hora , rut_empleado , num_mesa ,
			idmenu ) VALUES ('7','10/9/2018','19:00','12345678-8','18','pepi');
"""
cur.execute(sql)
sql="""
INSERT INTO pedidos (cant_atendida , fecha, hora , rut_empleado , num_mesa ,
			idmenu ) VALUES ('3','10/9/2018','17:00','12345678-5','15','pepi');
"""
cur.execute(sql)
sql="""
INSERT INTO pedidos (cant_atendida , fecha, hora , rut_empleado , num_mesa ,
			idmenu ) VALUES ('3','10/9/2018','13:00','12345678-5','15','colacion');
"""
cur.execute(sql)
sql="""
INSERT INTO pedidos (cant_atendida , fecha, hora , rut_empleado , num_mesa ,
			idmenu ) VALUES ('3','10/9/2018','14:00','12345678-5','12','colacion');
"""
cur.execute(sql)



conn.commit()
cur.close()
conn.close()
