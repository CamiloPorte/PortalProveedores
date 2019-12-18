#!/usr/bin/python
# -*- coding: utf-8 -*-
# Archivo ejemplo.py
class XMLMaker:

	def __init__(self):
		self.tag_stack = []
		self.string = ""
	def open_tag(self, tagname, **kwargs):
		#Abre un nuevo tag.
		#properties, text
		valid_keys = {"properties", "text"}
		for key in kwargs.keys():
			if key not in valid_keys:
				raise Exception("Este argumento de llave no es válido.")
		self.tag_stack.append(tagname)
		self.string += "<" + tagname
		if "properties" in kwargs:
			for k, v in kwargs["properties"].items():
				self.string += " %s='%s'" % (k, v)
		self.string += ">"
		if "text" in kwargs:
			self.string += kwargs["text"]
		return tagname
	def close_tag(self):
		#Cierra el último stack abierto.
		if len(self.tag_stack) == 0:
			raise Exception("No hay ningún tag abierto.")
		tagname = self.tag_stack.pop()
		self.string += "</%s>" % tagname
	def open_close_tag(self, tagname, **kwargs):
		#Abre un tag y lo cierra inmediatamente
		self.open_tag(tagname, **kwargs)
		self.close_tag()
		return tagname
	def finish(self):
		#Cierra todos los tags abiertos automáticamente.
		while len(self.tag_stack) != 0:
			self.close_tag()
	def __str__(self):
		return self.string