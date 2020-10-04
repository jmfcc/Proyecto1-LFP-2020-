import SQL_CLI

hist = []

dictLexm = {
    "create":["tk_create", "Indica que se debe crear un elemento"],
    "use":["tk_use", "Indica que se va a utilizar un set"],
    "set":["tk_set", "Es parte del comando create y use"],
    "idset":["tk_idset", "Es un id no definido (es decir un lexema del lenguaje, pero no considerado como reservado)"],
    "list":["tk_list", "Indica que el comando listara elementos"],
    "attributes":["tk_atrb", "Parte del comando list que indica que se listarán los atributos del set en uso"],
    "print":["tk_print", "Indica una modificación al momento de mostrar mensajes en consola"],
    "in":["tk_in", "Parte del comando print que hace referencia al color de fuente"],
    "color":["tk_color", "Es un lexema no reservado, puede obtener los valores de blue, green, red, entre otros"],
    "max":["tk_max", "Indica un valor maximo, tanto para valores numericos, cadenas o booleanos"],
    "min":["tk_min", "Indica un valor minimo, tanto para valores numericos, cadenas o booleanos"],
    "atrbset":["tk_attr", "Indica un lexema no reservado del atributo de un set"],
    ",":["tk_comma", "Es un separador de elementos"],
    "sum":["tk_sum", "Indica la sumatoria de un conjunto numerico (unicamente para numeros)."],
    "count":["tk_count", "Indica el conteo en los registro de los atributos del set en uso"],
    "*":["tk_astrsk", "Para valores de búsqueda indica que se utilizarán todos los atributos de un set"],
    "load":["tk_load", "Indica una carga, referente a un conjunto de registros que debe ser almacenado en memoria"],
    "into":["tk_into", "Hace referencia al concepto de indicar el set donde debe ser cargado los registros"],
    "files":["tk_files", "Indica que a continuación vendrán los archivos o ficheros que deberán ser leidos"],
    ".aon":["tk_AON", "Lexema no reservado que indica el nombre del archivo a cargar (Este siempre debe ser de extension .aon)"],
    "report":["tk_rep", "Indica que se generará un reporte"],
    "tokens":["tk_tokens", "Parte del comando report, que indica que se generará un reporte de los tokens leidos por el afd"],
}

def regHist(listCommand):
    if listCommand[0] == "create":
        for tk in listCommand:
            lt = []
            lt.append(tk)
            try:
                lt.extend(dictLexm[tk])
            except:
                lt.extend(dictLexm["idset"])
            hist.append(lt.copy())
    elif listCommand[0] == "use":
        for tk in listCommand:
            lt = []
            lt.append(tk)
            try:
                lt.extend(dictLexm[tk])
            except:
                lt.extend(dictLexm["idset"])
            hist.append(lt.copy())
    elif listCommand[0] == "list":
        for tk in listCommand:
            lt = []
            lt.append(tk)
            lt.extend(dictLexm[tk])
            hist.append(lt.copy())
    elif listCommand[0] == "print":
        for tk in listCommand:
            lt = []
            lt.append(tk)
            try:
                lt.extend(dictLexm[tk])
            except:
                lt.extend(dictLexm["color"])
            hist.append(lt.copy())
    elif listCommand[0] == "max":
        for tk in listCommand:
            lt = []
            lt.append(tk)
            try:
                lt.extend(dictLexm[tk])
            except:
                lt.extend(dictLexm["atrbset"])
            hist.append(lt.copy())
    elif listCommand[0] == "min":
        for tk in listCommand:
            lt = []
            lt.append(tk)
            try:
                lt.extend(dictLexm[tk])
            except:
                lt.extend(dictLexm["atrbset"])
            hist.append(lt.copy())
    elif listCommand[0] == "sum":
        ltm = []
        ltm.append(listCommand[0])
        ltm.extend(dictLexm[listCommand[0]])
        hist.append(ltm.copy())

        tm = len(listCommand) - 1
        inicio = True
        for tk in listCommand[tm]:
            lt = []
            if not inicio:
                lt.append(",")
                lt.extend(dictLexm[","])
                hist.append(lt.copy())
                lt.clear()
            else:
                inicio = False
                
            lt.append(tk)
            try:
                lt.extend(dictLexm[tk])
            except KeyError:
                lt.extend(dictLexm["atrbset"])
            hist.append(lt.copy())
    elif listCommand[0] == "count":
        ltm = []
        ltm.append(listCommand[0])
        ltm.extend(dictLexm[listCommand[0]])
        hist.append(ltm.copy())

        tm = len(listCommand) - 1
        inicio = True
        for tk in listCommand[tm]:
            lt = []
            if not inicio:
                lt.append(",")
                lt.extend(dictLexm[","])
                hist.append(lt.copy())
                lt.clear()
            else:
                inicio = False

            lt.append(tk)
            try:
                lt.extend(dictLexm[tk])
            except KeyError:
                lt.extend(dictLexm["atrbset"])
            hist.append(lt.copy())
    elif listCommand[0] == "load":
        for i in range(0, 4):
            ltm = []
            ltm.append(listCommand[i])
            try:
                ltm.extend(dictLexm[listCommand[i]])
            except KeyError:
                ltm.extend(dictLexm["idset"])
            hist.append(ltm.copy())

        tm = len(listCommand) - 1
        inicio = True
        for tk in listCommand[tm]:
            lt = []
            if not inicio:
                lt.append(",")
                lt.extend(dictLexm[","])
                hist.append(lt.copy())
                lt.clear()
            else:
                inicio = False

            lt.append(tk)
            try:
                lt.extend(dictLexm[tk])
            except KeyError:
                lt.extend(dictLexm[".aon"])
            hist.append(lt.copy())
    elif listCommand[0] == "report": # Incompleto (Solo Report Tokens)
        for tk in listCommand:
            lt = []
            lt.append(tk)
            lt.extend(dictLexm[tk])
            hist.append(lt.copy())
        
def getHisto():
    return hist

def muestraHist():
    for h in hist:
        print(h)