#!/usr/bin/env python

import subprocess
import optparse
import re

def tomar_argumentos():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interfaz", dest="interfaz", help="Interfaz en la que cambiara la direccion MAC.")
    parser.add_option("-m", "--mac", dest="nueva_mac", help="Direccion MAC deseada.")

    (opciones,argumentos) = parser.parse_args()

    if not opciones.interfaz and not opciones.nueva_mac:
        parser.error("[-] Especifica la interfaz y la direccion MAC deseada.")
    elif not opciones.interfaz:
        parser.error ("[-] Especifica la interfaz a la que quieres modificarle la direccion MAC. Usa '-h' o '--help' para mas info.")
    elif not opciones.nueva_mac:
        parser.error ("[-] Especifica una nueva direccion MAC. Usa '-h' o '--help' para mas info.")

    return opciones

def cambiar_mac (interfaz,nueva_mac):
    print ("[+] Cambiando direccion MAC de {} a {}...".format(interfaz, nueva_mac))
    subprocess.call(["ifconfig", interfaz, "down"])
    subprocess.call(["ifconfig", interfaz, "hw", "ether", nueva_mac])
    subprocess.call(["ifconfig", interfaz, "up"])

def tomar_mac_actual (interfaz):
    ifconfig_result = subprocess.check_output(["ifconfig", interfaz])
    resultado_busqueda = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if resultado_busqueda:
        return resultado_busqueda.group(0)

    else:
        print("[-] No se pudo leer la direccion MAC. Escoge una interfaz valida.")

opciones = tomar_argumentos()
mac_actual = tomar_mac_actual(opciones.interfaz)
print ("MAC actual = " + str(mac_actual)) #Casting de mac_actual
cambiar_mac(opciones.interfaz, opciones.nueva_mac)

mac_actual = tomar_mac_actual(opciones.interfaz)
if mac_actual == opciones.nueva_mac:
    print ("[+] La direccion MAC se modifico satisfactoriamente a " + mac_actual)
    print ("[+] Happy hack. @YeguaCelestial")

else:
    print ("[-] No fue posible cambiar la direccion MAC. Usa '--help' o '-h' para mas informacion.")