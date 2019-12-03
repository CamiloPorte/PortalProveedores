#!/usr/bin/python
# -*- coding: utf-8 -*-
# Archivo ejemplo.py

from app import app
from flask import render_template,request,redirect
import numpy as np
from ctypes import *

 


@app.route('/', methods=["POST", "GET"])
def formulario():
	libmean = CDLL('./libmean.so')
	conexion = libmean.conexion
	conexion.argtypes = []
	conexion.restype = c_char_p
	contar = libmean.contar
	contar.argtypes = [c_int, c_char_p , c_wchar]
	contar.restype = c_int
	texto = conexion()
	print(texto)
	filas = contar(len(texto),texto,'~') 
	matriz = []
	aux = []
	ans =[]
	ciclos = 0

	datos = str(texto).split('|')
	aux.append(datos[0].split("'")[1])
	for i in range(filas+1):
	    for j in range(1,3):
	    	aux.append(datos[j+ciclos])
	    ciclos = ciclos + 3
	    aux.append(datos[ciclos].split('~')[0])
	    matriz.append(aux)
	    aux =[]
	    if i <filas:
 	   		aux.append(datos[ciclos].split('~')[1])
	

	for i in range(len(matriz)):
		if i < len(matriz)-1:
			if matriz[i][0] != matriz[i+1][0]:
				ans.append(matriz[i])
		else:
			print(matriz[i])
			ans.append(matriz[i])
	print(ans)
	return render_template("tables.html",matriz=ans)





