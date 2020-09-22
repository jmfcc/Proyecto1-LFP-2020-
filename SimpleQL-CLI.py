import time
import json
import os
import reporte
from AONanalyzer import analizadorAON

sets = []
dbsets = {}

def dbempty():
    if len(dbsets) == 0:
        return False
    else:
        return True

def AONload(setload, listf):
    for f in listf:
        if os.path.isfile(f):
            ph, fh = os.path.split(f)
            nombre, extension = os.path.splitext(fh)
            if extension.__eq__(".json"):
                files = open(f)
                datosjson = json.load(files) #Se carga los datos como diccionarios
                #db.append(datosjson)
                db.extend(datosjson)
                #print(db)
                time.sleep(1)
                print(" -- Carga Completa -- ", nombre + extension,"\n")
            else:
                print(" -- El archivo no es de extensión .json -- ")
        else:
            print(" -- Fichero no encontrado -- ")


#cargar()

def select(solicitud, busqueda): #SELECCIONAR x, y, z/* DONDE n = m
    if not dbempty():
        if busqueda:
            find = False
            muestraencabezado = True
            for registro in db:
                #print("\n", busqueda, "\n")
                #print("valida item")
                if registro[busqueda[0]] == busqueda[1]:
                    find = True
                    if solicitud == "*":
                        reg = []
                        reg.extend(registro.items())
                        separa = separadorvertical(solicitud)
                        if muestraencabezado:
                            print("\n")
                            print(aniadeespacio(" -- NOMBRE --") + "||" + aniadeespacio(" -- EDAD --") + "||" + aniadeespacio(" -- ACTIVO --")+ "||" + aniadeespacio(" -- PROMEDIO --") + "||")
                            print(separa)
                            muestraencabezado = False
                        rowprint = ""
                        init = True
                        for r in reg:
                            if init:
                                rowprint = aniadeespacio(r[1]) + "||"
                                init = False
                            else:
                                rowprint = rowprint + aniadeespacio(r[1]) + "||"
                        print(rowprint)
                        print(separa)
                            #print(r[0], ": ", r[1])  #, "   Type: ", type(r[1])
                    else:
                        separa = separadorvertical(solicitud)
                        if muestraencabezado:
                            print("\n")
                            encab = ""
                            init = True
                            for itm in solicitud:
                                if init:
                                    encab = aniadeespacio(" -- " + itm.upper() + " --")
                                    init = False
                                else:
                                    encab = encab + aniadeespacio(" -- " + itm.upper() + " --")
                            print(encab)
                            print(separa)
                            muestraencabezado = False
                        rowprint = ""
                        init = True
                        for s in solicitud:
                            if init:
                                rowprint = aniadeespacio(registro[s]) + "||"
                                init = False
                            else:
                                rowprint = rowprint + aniadeespacio(registro[s]) + "||"
                            #print(s, ": ", registro[s])  #, "   Type: ", type(registro[s])
                            #datos.append(registro[s])
                        print(rowprint)
                        print(separa)
                    #print()
                elif busqueda[0] == "nombre" and registro[busqueda[0]].lower() == busqueda[1]:
                    find = True
                    if solicitud == "*":
                        reg = []
                        reg.extend(registro.items())
                        separa = separadorvertical(solicitud)
                        if muestraencabezado:
                            print("\n")
                            print(aniadeespacio(" -- NOMBRE --") + "||" + aniadeespacio(" -- EDAD --") + "||" + aniadeespacio(" -- ACTIVO --")+ "||" + aniadeespacio(" -- PROMEDIO --") + "||")
                            print(separa)
                            muestraencabezado = False
                        rowprint = ""
                        init = True
                        for r in reg:
                            if init:
                                rowprint = aniadeespacio(r[1]) + "||"
                                init = False
                            else:
                                rowprint = rowprint + aniadeespacio(r[1]) + "||"
                        print(rowprint)
                        print(separa)
                    else:
                        separa = separadorvertical(solicitud)
                        if muestraencabezado:
                            print("\n")
                            encab = ""
                            init = True
                            for itm in solicitud:
                                if init:
                                    encab = aniadeespacio(" -- " + itm.upper() + " --")
                                    init = False
                                else:
                                    encab = encab + aniadeespacio(" -- " + itm.upper() + " --")
                            print(encab)
                            print(separa)
                            muestraencabezado = False
                        rowprint = ""
                        init = True
                        for s in solicitud:
                            if init:
                                rowprint = aniadeespacio(registro[s]) + "||"
                                init = False
                            else:
                                rowprint = rowprint + aniadeespacio(registro[s]) + "||"
                            #print(s, ": ", registro[s])  #, "   Type: ", type(registro[s])
                            #datos.append(registro[s])
                        print(rowprint)
                        print(separa)
                    #print()
            if not find:
                print (" -- NINGUNA COINCIDENCIA -- ")
        elif solicitud == "*":
            print("\n")
            separa = separadorvertical(solicitud)
            print(aniadeespacio(" -- NOMBRE --") + "||" + aniadeespacio(" -- EDAD --") + "||" + aniadeespacio(" -- ACTIVO --")+ "||" + aniadeespacio(" -- PROMEDIO --") + "||")
            print(separa)
            for registro in db:
                reg = []
                reg.extend(registro.items())
                rowprint = ""
                init = True
                for r in reg:
                    if init:
                        rowprint = aniadeespacio(r[1]) + "||"
                        init = False
                    else:
                        rowprint = rowprint + aniadeespacio(r[1]) + "||"
                print(rowprint)
                print(separa)
        else:
            print("\n")
            separa = separadorvertical(solicitud)
            encab = ""
            init = True
            for itm in solicitud:
                if init:
                    encab = aniadeespacio(" -- " + itm.upper() + " --")
                    init = False
                else:
                    encab = encab + aniadeespacio(" -- " + itm.upper() + " --")
            print(encab)
            print(separa)
            for registro in db:
                rowprint = ""
                init = True
                for s in solicitud:
                    if init:
                        rowprint = aniadeespacio(registro[s]) + "||"
                        init = False
                    else:
                        rowprint = rowprint + aniadeespacio(registro[s]) + "||"
                    #print(s, ": ", registro[s])  #, "   Type: ", type(registro[s])
                    #datos.append(registro[s])
                print(rowprint)
                print(separa)
    else:
        print(" -- NO HAY REGISTROS EN MEMORIA -- ")

def separadorvertical(n):
    try:
        if n == "*":
            n = ["*", "*", "*", "*"]
    except:
        pass
    sep = ""
    init = True
    for i in range(0, len(n)):
        if init:   
            sep = "--------------------------------||"
            init = False
        else:
            sep = sep + "--------------------------------||"
    return sep

def aniadeespacio(elemento):
    elem = str(elemento)
    k = 32
    k = k - len(elem)
    spaces = ""
    for i in range(0, k):
        spaces = spaces + " "
    elem = elem + spaces
    return elem
    
#req = ["nombre", "edad", "promedio"]
#reqall = "*"
#busq = ["nombre", "registro 3"]
#busq2 = ["promedio", 60.5]
#b = ""
#seleccion(reqall, b)

def getmaximo(tipo): #MAXIMO edad/promedio
    maximo = 0
    init = True
    for registro in db:
        if init:
            maximo = registro[tipo]
            init = False
        else:
            if maximo < registro[tipo]:
                maximo = registro[tipo]
    print(tipo, ": ", maximo)

#max("promedio")

def getminimo(tipo): #MINIMO edad/promedio
    minimo = 0
    init = True
    for registro in db:
        if init:
            minimo = registro[tipo]
            init = False
        else:
            if minimo > registro[tipo]:
                minimo = registro[tipo]
    print(tipo, ": ", minimo)

#min("edad")

def suma(tipo): #SUMA edad/promedio
    sumatoria = 0
    init = True
    for registro in db:
        if init:
            sumatoria = registro[tipo]
            init = False
        else:
            sumatoria = sumatoria + registro[tipo]
    print(tipo, ": ", sumatoria)

#suma("promedio")

def cont(): #CUENTA
    print("# Registros: ", len(db))

#cont()

def reportar(n):
    print(" -- Generando Reporte -- ")
    time.sleep(1)
    reporte.reporte(db, n)

def dblength():
    return len(db)


# cargar PYTHON\2S 2020\201709020_PracticaLFP\ejemplo.json, PYTHON\2S 2020\201709020_PracticaLFP\ejemplo2.json