Instrucciones:

Instalar:
-psycopg2
-Python 3
-WTForms
-Werkzeug
-Postresql

Para configurar la base de datos con lo necesario para el proyecto se debe seguir los siguientes pasos:

Escribir: 
	sudo su - postgres
Ingresar contraseña del usuario actual del pc (la clave del computador). 

Escribir:
	psql
Se debe ingresar la clave de Postgres, por default la clave es “postgres".

Posteriormente se debe crear el usuario “qa” con contraseña “pesaschile”. Para lo anterior se debe ingresar el siguiente comando:
	CREATE USER qa WITH password ‘pesaschile’;

Ya con el usuario creado, se debe crear la base de datos “pesaschile” con dueño “qa”, para eso se debe ingresar:
	CREATE DATABASE pesaschile WITH OWNER qa;

Ya con la base de datos creada, para ingresar a la base de datos con el usuario “qa” se utiliza el siguiente comando:
	psql -U qa pesaschile
Posteriormente, se solicita la clave que, en nuestro caso es “pesaschile”, al ingresarla, ya estará dentro de la base y podrás escribir consultas directamente para obtener información o probar las consultas en desarrollo.