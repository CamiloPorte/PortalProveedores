import app.tcputils as tcp
import xml.etree.ElementTree as ET
from app.xmlutils import XMLMaker

TCP_IP = "45.79.37.223"
TCP_PORT = 25000

def get_ott(xmlstring):
    return ET.fromstring(xmlstring).find("ott").text

def get_dat(xmlstring):
	return ET.fromstring(xmlstring).find("info").find("dat").text

#Conectar
s = tcp.connect(TCP_IP, TCP_PORT)
message = "<tx id='borja'><req>auten</req><usr>walker</usr><psw>walker</psw></tx>"
tcp.send(s, message)
#Obtener respuesta OTT
xml_received = tcp.receive(s)
ott_id = get_ott(xml_received)
#Crear xml query
xml_maker = XMLMaker()
xml_maker.open_tag("tx", properties={"id": "borja"})
xml_maker.open_close_tag("req", text="dbcurXML")
xml_maker.open_close_tag("ott", text=str(ott_id))
xml_maker.open_tag("prm")
sql_query = "select emp!01, por!02 from cuelogs"
xml_maker.open_tag("sql", text=sql_query)
xml_maker.finish()
xml_request = str(xml_maker)
#Enviar xml
tcp.send(s, xml_request)
xml_received = tcp.receive(s)
print("response: ", xml_received)