from os import path

alfabeto = ["(", ")", "<", ">", "[", "]", ",", "\"", "=", "default"]
elementos = {
    "(" : "tk_parentesisInicio",
    ")" : "tk_parentesisCierre", 
    "<" : "tk_flechaInic", 
    ">" : "tk_flechaCierre", 
    "[" : "tk_llaveInicio", 
    "]" : "tk_llaveCierre", 
    "=" : "tk_asignacion",
    "bool" : "tk_boolean", 
    "letras" : "tk_str", 
    "numeros" : "tk_numeric", 
    "," : "tk_coma",
    "\"" : "tk_comillas",
    "default" : "None"
    }

transiciones = [
    ["0", "(", "1"],
    ["1", "<", "2"],
    ["2", "[", "3"],

    ["3", "letras", "4"],
    ["4", "letras", "4"],

    ["4", "]", "5"],
    ["5", "=", "6"],


    ["6", "\"", "7"],
    ["7", "letras", "8"],
    ["8", "letras", "8"],
    ["8", " ", "8"],
    ["8", "\"", "9"],

    ["9", ",", "10"],

    ["6", "-", "7"],
    ["6", "numero", "7"],
    ["7", "numero", "7"],
    ["7", ".", "7"],

    ["6", "textbool", "7"],
    ["7", "textbool", "7"],
    ["7", ",", "10"],

    ["10", "[", "3"],

    ["9", ">", "11"],
    ["7", ">", "11"],

    ["11", ",", "12"],
    ["12", "<", "2"],

    ["11", ")", "13"]
    ]

def getsource():
    ruta = path.dirname(path.abspath(__file__)) #Obtiene la ruta del script en ejecución
    #archivo = open(ruta + "/archivo.csv")
    return ruta



#def analizadorAON():
    #ruta = getsource() + "/archivoprueba.aon"
def analizadorAON(nombrearchivo):
    db = []
    tipotoken = []
    #db.clear()
    ruta = getsource() + "/" + nombrearchivo
    file = open(ruta, "r")

    estadoActual = "0"
    registratoken = False
    estadoSiguiente = ""
    ignorespaces = True
    tokenalmacenado = False
    token = ""
    listdict = [] #[["precio", 45.23],["desc", "adios etc"]]
    listakeyitem = []    #["precio", -45.23]
    dicctemp = {}

    #tokenread = ""

    for line in file:
        for char in line:
            #tokenread = char
            if ignorespaces:
                if not char.isspace():    #analisis de elementos sin espacios -------------------------------
                    tokenalmacenado = False #
                    if char == "[":   #empieza un atributo del diccionario
                        if estadoActual == "2" or estadoActual == "10":
                            #token = char
                            ignorespaces = False
                            registratoken = True
                            estadoSiguiente = validaTransicion(estadoActual, char)
                        else:
                            estadoSiguiente = "None"
                    elif char == "\"": # empieza una cadena de texto
                        if estadoActual == "6":
                            #token = char
                            ignorespaces = False
                            registratoken = True
                            estadoSiguiente = validaTransicion(estadoActual, char)
                        else:
                            estadoSiguiente = "None"
                    elif char.isdigit():  # analiza un valor numerico
                        if estadoActual == "6":
                            token = char
                            estadoActual = validaTransicion(estadoActual, "numero")
                        elif estadoActual == "7":
                            token = token + char
                            estadoActual = validaTransicion(estadoActual, "numero")
                        else:
                            estadoSiguiente = "None"
                    elif char == "-":   # analiza si inicia un valor numerico negativo
                        if estadoActual == "6":
                            token = char
                            estadoActual = validaTransicion(estadoActual, char)
                        else:
                            estadoSiguiente = "None"
                    elif char == ".": # analiza una transicion con punto decimal
                        if estadoActual == "7":
                            token = token + char
                            estadoActual = validaTransicion(estadoActual, char)
                        else:
                            estadoSiguiente = "None"
                    elif char.isalpha():
                        if estadoActual == "6":
                            token = char
                            estadoActual = validaTransicion(estadoActual, "textbool")
                        elif estadoActual == "7":
                            token = token + char
                            estadoActual = validaTransicion(estadoActual, "textbool")
                        else:
                            estadoSiguiente = "None"
                    elif char == "," and estadoActual == "7":
                        if not token.isspace():
                            try:
                                token = float(token)
                                
                                listakeyitem.append(token)
                                #print(listakeyitem)
                                listdict.append(listakeyitem.copy())
                                listakeyitem.clear()
                                #print(listdict)

                                tipotoken.append(str(token) + " <--- " + elementos["numeros"])
                                #estadoActual = estadoSiguiente
                                tokenalmacenado = True
                            except :
                                if token == "false":

                                    listakeyitem.append(False)
                                    #print(listakeyitem)
                                    listdict.append(listakeyitem.copy())
                                    listakeyitem.clear()

                                    tipotoken.append("False" + " <--- " + elementos["bool"])
                                    tokenalmacenado = True
                                elif token == "true":

                                    listakeyitem.append(True)
                                    #print(listakeyitem)
                                    listdict.append(listakeyitem.copy())
                                    listakeyitem.clear()

                                    tipotoken.append("True" + " <--- " + elementos["bool"])
                                    tokenalmacenado = True
                                else:
                                    print (" ------ Error en valor asignado -------- ", type(token))
                                    return
                                #estadoActual = estadoSiguiente
                            token = " " #limpiamos el token --------------------------
                        registratoken = True
                        estadoSiguiente = validaTransicion(estadoActual, char)
                    elif char == "," and estadoActual == "9": #2 casos que venga "23.3", | "23.3" ,
                        registratoken = True
                        estadoSiguiente = validaTransicion(estadoActual, char)
                    elif char == "," and estadoActual == "11":
                        registratoken = True
                        estadoSiguiente = validaTransicion(estadoActual, char)
                    elif alfabeto.__contains__(char):
                        if char == ">":
                            if not token.isspace():
                                try:
                                    token = float(token)
                                    #print(token, "    ", type(token))
                                    listakeyitem.append(token)
                                    listdict.append(listakeyitem.copy())
                                    listakeyitem.clear()

                                    tipotoken.append(str(token) + " <--- " + elementos["numeros"])
                                    #estadoActual = estadoSiguiente
                                    tokenalmacenado = True
                                except :
                                    if token == "false":

                                        listakeyitem.append(False)
                                        listdict.append(listakeyitem.copy())
                                        listakeyitem.clear()

                                        tipotoken.append("False" + " <--- " + elementos["bool"])
                                        tokenalmacenado = True
                                    elif token == "true":

                                        listakeyitem.append(True)
                                        listdict.append(listakeyitem.copy())
                                        listakeyitem.clear()

                                        tipotoken.append("True" + " <--- " + elementos["bool"])
                                        tokenalmacenado = True
                                    else:
                                        print (" ------ Error en valor asignado -------- ", token, " - ", char, " -  ", estadoActual, "  " , estadoSiguiente)
                                        return
                                    #estadoActual = estadoSiguiente
                                token = " "
                            if estadoActual == "7" or estadoActual == "9":
                                # almacenar el diccionario ------------------------------------
                                #print(listdict)
                                for itm in listdict:
                                    dcn = {itm[0] : itm[1]}
                                    dicctemp.update(dcn) #se añaden los items al diccionario
                                listdict.clear()
                                listakeyitem.clear()
                                db.append(dicctemp.copy()) # se agrega el diccionario a la base de datos
                                dicctemp.clear() # se limpia el diccionario temporal
                            else:
                                print(" ------------ Error lexico -----------   ", token, char)
                                return
                        elif char == ")":
                            print("  -- Archivo Cargado -- ... ")
                        token = " "
                        registratoken = True
                        estadoSiguiente = validaTransicion(estadoActual, char)
                    else:
                        print(" ------------ Error lexico -----------   ", token, "  ", char, "   ", estadoActual, "  " , estadoSiguiente)
                        return

                    if estadoSiguiente == "None":
                        print(" ------------ Error de sintaxis -----------   ", token, "  ", char, "   ", estadoActual, "  " , estadoSiguiente)
                        return
                    #elif not registratoken:
                    #    estadoActual = estadoSiguiente
                    
                    if registratoken: #algo que indique si necesito hacer un cast a int o manejar booleanos
                        tipotoken.append(char + " <--- " + elementos[char])
                        estadoActual = estadoSiguiente
                        registratoken = False
                        tokenalmacenado = True

                #correccion de tokens con espacios
                #ocurre cuando char es espacio -----------------------------------
                elif not tokenalmacenado: # fin de un token y analisis del mismo
                    if not token.isspace():
                        try:
                            token = float(token)
                            #print(token, "    ", type(token))
                            listakeyitem.append(token)
                            listdict.append(listakeyitem.copy())
                            listakeyitem.clear()

                            tipotoken.append(str(token) + " <--- " + elementos["numeros"])
                            #estadoActual = estadoSiguiente
                            tokenalmacenado = True
                        except :
                            if token == "false":

                                listakeyitem.append(False)
                                listdict.append(listakeyitem.copy())
                                listakeyitem.clear()

                                tipotoken.append("False" + " <--- " + elementos["bool"])
                                tokenalmacenado = True
                            elif token == "true":

                                listakeyitem.append(True)
                                listdict.append(listakeyitem.copy())
                                listakeyitem.clear()

                                tipotoken.append("True" + " <--- " + elementos["bool"])
                                tokenalmacenado = True
                            else:
                                print (" ------ Error en valor asignado -------- ", token, " - ", char, " -  ", estadoActual, "  " , estadoSiguiente)
                                return
                            #estadoActual = estadoSiguiente
                        token = " " #limpiamos el token --------------------------
            else:
                if char.isalpha() and (estadoActual == "3" or estadoActual == "4"):
                    if estadoActual == "3":
                        token = char
                    elif estadoActual == "4":
                        token = token + char
                    estadoActual = validaTransicion(estadoActual, "letras")
                elif (char.isalpha() or char.isdigit()) and (estadoActual == "7" or estadoActual == "8"):
                    if estadoActual == "7":
                        token = char
                    elif estadoActual == "8":
                        token = token + char
                    estadoActual = validaTransicion(estadoActual, "letras")
                elif char == " " and estadoActual == "4":
                    pass
                elif char == " " and estadoActual == "8":
                    token = token + char
                    estadoSiguiente = validaTransicion(estadoActual, " ")
                elif char == "]" and estadoActual == "4": # fin de nombre de atributo -----------------
                    listakeyitem.append(token)
                    #print(token, " --------------- key")
                    tipotoken.append(token + " <--- " + elementos["letras"])
                    
                    estadoActual = validaTransicion(estadoActual, char)
                    
                    tipotoken.append(char + " <--- " + elementos[char])
                    ignorespaces = True
                    
                    token = " "
                elif char == "\"" and estadoActual == "8":  # fin de valor --------------------------
                    listakeyitem.append(token)
                    listdict.append(listakeyitem.copy())
                    listakeyitem.clear()
                    tipotoken.append(token + " <--- " + elementos["letras"])
                    
                    estadoActual = validaTransicion(estadoActual, char)
                    
                    tipotoken.append(char + " <--- " + elementos[char])

                    ignorespaces = True
                    token = " "
                else:
                    print("Error de lexico en cadena o id")
                    return
    print()
    #print(db)
    #for ttk in tipotoken:
    #    print(ttk)
    if estadoActual == "13":
        return db
    else:
        return None

                
            
    
def validaTransicion(estadoA, simbolo):
    for tr in transiciones:
        if tr[0] == estadoA and tr[1] == simbolo:
            estadoS = tr[2]
            return estadoS
    return "None"

def prueba():
    ruta = getsource() + "/archivoprueba.aon"
    file = open(ruta, "r")

    for line in file:
        print (line)


#analizadorAON()
#print
#for diccion in db:
#    try:
#        print(diccion["prueba"])
#    except KeyError:
#        print("no existe un atributo prueba")