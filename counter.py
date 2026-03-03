# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 20:46:52 2025

Este fichero contiene una serie de funciones para la realización de conteos y 
estadísticas sobre los ficheros cupt del corpus. 

Función principal: print_data(corpus_path, lan_to_print)

@author: sflan
"""

import tools
import os

"""
Imprime todos los conteos de un idioma (si se especifica el idioma concreto)
o de todos los idiomas si no se especifica el idioma o bien se especifica como 
"ALL". Los datos se desglosan de la siguiente forma:
    
    1.- Para el fichero train.cupt
        1.1.- Sección SENTENCES:
            1.1.1.- Número de oraciones desglosado por número de tokens de la 
                    oración. Por ejemplo, el corpus EU tiene 4 oraciones con 2 
                    tokens, 44 oraciones con 3 tokens, 91 oraciones con 4 
                    tokens, ...:
                        
                        Num_tok	   	Num_sent
                                	EU
                        2   	   	   	4
                        3   	   	   	44
                        4   	   	   	91
                        ...
                        
            1.1.2.- Número de oraciones desglosado por número de MWEs de la 
                    oración. Por ejemplo, el corpus EU tiene 3257 oraciones 
                    con 0 MWEs, 1157 oraciones con 1 MWE, 225 oraciones con 2 
                    MWEs, ...:
                        
                        Num_MWEs	Num_sent
                            	   	   	EU
                        0   	   	   	3257
                        1   	   	   	1157
                        2   	   	   	225
                        3   	   	   	35
                        4   	   	   	8
                        5   	   	   	2
                        TOTAL	   	4684
                        
        1.2.- Seccion TOKENS:
            1.2.1.- Número de tokens desglosado por número de caracteres del 
                    texto del token. Por ejemplo, el corpus EU tiene 10695 
                    tokens con 1 caracter, 2975 tokens con 2 caracters, 5569 
                    tokens con 3 caracters, ...:
                        
                        Num_chars	Num_tok
                        	   	   	   	EU
                        1	   	   	   	10695
                        2	   	   	   	2975
                        3	   	   	   	5569
                        ...
                
            1.2.2.- Número de tokens con información sobre MWEs (se excluyen 
                    de la cuenta los tokens que tienen "*") desglosado por el 
                    número de caracteres de la etiqueta MWE del token. Por 
                    ejemplo, el corpus EU tiene 1757 tokens con 1 caracter en 
                    su etiqueta MWE, 11 tokens con 3 caracteres en su etiqueta 
                    MWE, 357 tokens con 5 caracteres en su etiqueta MWE, ...:
                        
                        Num_chars_MWE	Num_tok
                        	   	   	   	   	EU
                        1	   	   	   	   	1757
                        3	   	   	   	   	11
                        5	   	   	   	   	357
                        ...

            1.2.3.- Número de tokens desglosado por número de MWEs a las que 
                    pertenece el token. Por ejemplo, el corpus EU tiene 63313 
                    tokens que no pertenecen a ninguna MWE, 3499 tokens que 
                    pertenecen a 1 MWE y 21 tokens que pertenecen a 2 MWEs:
                        
                        Num_MWEs	Num_tok
                        	   	   	   	EU
                        0	   	   	   	63313
                        1	   	   	   	3499
                        2	   	   	   	21
                        TOTAL	   	66833
                
        1.3.- Sección MWEs:
            1.3.1.- Número de MWEs desglosado por número de tokens que tiene 
                    la MWE. Por ejemplo, el corpus EU tiene 1724 MWEs de 2 
                    tokens, 27 MWEs de 3 tokens y 3 MWEs de 4 tokens:
                        
                        Num_tok	Num_MWEs
                        	   	   	EU
                        2	   	   	1724
                        3	   	   	27
                        4	   	   	3
                        TOTAL	1754
                        
            1.3.2.- Número de MWEs desglosado por el tipo de etiqueta que 
                    tiene la MWE. Por ejemplo, el corpus EU tiene 92 MWEs 
                    LVC.cause, 1304 MWEs LVC.full y 358 MWEs VID:
                        
                        Label	   	Num_MWEs
                        	   	   	   	EU
                        LVC.cause	92
                        LVC.full	1304
                        VID	   	   	358
                        TOTAL	   	1754
            
            1.3.3.- Número de MWEs desglosado por el tipo de MWE según si es 
                    cruzada o anidada (sin considerar solapamiento en los 
                    extremos). 
                    
                    Sean dos MWEs A = [t_1, ...t_n] y B = [s_1, ...s_m], donde 
                    los t_i son las posiciones de los tokens de la MWE A y los 
                    s_i las posiciones de los tokens de la MWE B:
                    
                    * CRUZADAS: En este apartado se considera que A y B están 
                      cruzadas (sin considerar solapamiento) ssi:
                          t_1 < s_1 and s_1 < t_n and t_n < s_m
                    * ANIDADAS: En este apartado se considera que A y B están 
                      anidadas (sin considerar solapamiento) ssi:
                          t_1 < s_1 and s_1 < s_m and s_m < t_n
                    
                    Por ejemplo, considerando las definiciones anteriores el 
                    corpus ES tiene 1724 MWEs ni cruzadas ni anidadas, 6 MWEs 
                    cruzadas y 2 MWEs anidadas:
                        
                        Cross/Nest(str)	Num_MWEs
                        	                ES
                        -	                1724
                        c	                6
                        n	                2
                        TOTAL	          1732

            1.3.4.- Número de MWEs desglosado por el tipo de MWE según si es 
                    cruzada o anidada (sin considerar ningún tipo de 
                    solapamiento). 
                    
                    Sean dos MWEs A = [t_1, ...t_n] y B = [s_1, ...s_m], donde 
                    los t_i son las posiciones de los tokens de la MWE A y los 
                    s_i las posiciones de los tokens de la MWE B:
                    
                    * CRUZADAS: En este apartado se considera que A y B están 
                      cruzadas (sin considerar ningún tipo de solapamiento) ssi:
                          t_1 < s_1 and s_1 < t_n and t_n < s_m  
                          and A intersección B = 0
                    * ANIDADAS: En este apartado se considera que A y B están 
                      anidadas (sin considerar solapamiento) ssi:
                          t_1 < s_1 and s_1 < s_m and s_m < t_n
                          and A intersección B = 0
                    
                    Por ejemplo, considerando las definiciones anteriores el 
                    corpus HR tiene 1329 MWEs ni cruzadas ni anidadas, 2 MWEs 
                    anidadas y 1 MWE doblemente anidada:
                        
                        Cross/Nest(none)	Num_MWEs
                                         HR
                        -	            1329
                        n	            2
                        nn	            1
                        TOTAL           1332

            1.3.5.- Número de MWEs desglosado por el tipo de MWE según si es 
                    cruzada o anidada (considerando solapamiento). 
                    
                    Sean dos MWEs A = [t_1, ...t_n] y B = [s_1, ...s_m], donde 
                    los t_i son las posiciones de los tokens de la MWE A y los 
                    s_i las posiciones de los tokens de la MWE B:
                    
                    * CRUZADAS: En este apartado se considera que A y B están 
                      cruzadas (considerando solapamiento) ssi:
                          t_1 < s_1 and s_1 <= t_n and t_n < s_m
                    * ANIDADAS: En este apartado se considera que A y B están 
                      anidadas (considerando solapamiento) ssi:
                          t_1 <= s_1 and s_1 < s_m and s_m <= t_n
                    
                    Por ejemplo, considerando las definiciones anteriores el 
                    corpus ES tiene 1318 MWEs ni cruzadas ni anidadas, 97 MWEs 
                    cruzadas (c), 3 MWEs doblemente cruzadas (cc), 11 que 
                    están cruzadas una MWE y anidadas con otra (cn), 269 MWEs 
                    anidadas (n) y 34 MWEs doblemente anidadas (nn):
                        
                        Cross/Nest(ovl)     Num_MWEs
                                            ES
                        -                   1318
                        c                   97
                        cc                  3
                        cn                  11
                        n                   269
                        nn                  34
                        TOTAL               1732
                    
                    NOTA: Respecto al cruzado y anidamiento puede haber muchas 
                          tipologías:
                              c: significa que una MWE está cruzada con otra
                              cc: significa que una MWE está cruzada con otra 
                                  y con una tercera
                              cn: significa que una MWE está cruzada con otra 
                                  y anidada con una tercera
                              cnn: significa que una MWE está cruzada con otra, 
                                   anidada con una tercera y anidada con una 
                                   cuarta
                              n: significa que una MWE está anidada con otra
                              nn: significa que una MWE está anidada con otra 
                                  y con una tercera
                              nnn: significa que una MWE está anidada con otra, 
                                   con una tercera y con una cuarta
                              ...
                        [Nota válida también para el apartado anterior 1.3.3]
              
            1.3.6.- Número de MWEs desglosado por la forma de compartir tokens.
                    Puede suceder que una MWE comparta tokens con varias MWEs 
                    y que no sólo comparta 1 token sino que puede compartir 
                    varios. Para representar eso separaremos con una barra 
                    vertical ("|") cada una de las MWEs involucradas y 
                    pondremos un número entre las barras indicando el número 
                    de tokens que comparte. Por ejemplo:
                        1: significa que la MWE comparte un token con otra
                        1|1: significa que la MWE comparte un token con otra 
                             y otro token con una tercera
                        1|1|1: significa que la MWE comparte un token con otra, 
                               otro token con una tercera y otro token con una 
                               cuarta
                        2|2|1: significa que la MWE comparte 2 token con otra, 
                               2 token con una tercera y otro token con una 
                               cuarta
                        ...
                    Por ejemplo, el corpus EU tiene 1723 MWEs que no comparten 
                    tokens (-), 20 MWEs que comparten un token con otras (1), 
                    1 MWE que comparte un token con una segunda y una 
                    tercera (1|1) y 10 MWEs que comparten 2 tokens con otra (2)
                        
                        Shared	Num_MWEs
                                EU
                        -       1723
                        1       20
                        1|1     1
                        2       10
                        TOTAL	1754
                    
    2.- Para el fichero dev.cupt: IDEM
    
    3.- Para el fichero test.cupt: IDEM

En el caso de que se realice el conteo sobre varios idiomas se hace un 
mezclado de las tablas ya que no todos los idiomas tienen que tener las mismas 
opciones en la primera columna. En el mezclado se hará la unión de las 
opciones de las primeras columnas de cada tabla y los valores se rellenaran 
en el caso que exista valor para esa opción y se dejará en blanco en caso de 
que no exista valor para esa opción

Entradas: 
    corpus_path: Path del directorio del corpus
    lan_to_print: Idioma sobre el que se quieren realizar los conteos. Si es 
                  "ALL" o no se especifica se realizan los conteos sobre todos
                  los idiomas del corpus    
Salidas: 
    void: Imprime por pantalla todas las tablas de los conteos 
"""
def print_data(corpus_path, lan_to_print):
    # Inicialización de variables
    all_train_data = {}
    all_dev_data = {}
    all_test_data = {}
    all_system_data = {}
    lans = ""
    flag = False
    # Listamos los subdirectorios del directorio del corpus que corresponden a 
    # cada uno de los idiomas
    lan_folders = os.listdir(corpus_path)
    # Recorremos todos los subdirectorios del directorio que corresponden a 
    # cada uno de los idiomas
    for lan in lan_folders:
        # Almacenamos todos los códigos de idiomas en una cadena. Sólo se 
        # utilizará en caso de que el usuario introduzca un código erróneo. 
        # En ese caso se le mostrará al usuario todas las opciones de idiomas 
        # disponibles
        lans = lans + lan + ", "
        # Si el nombre del fichero (lan) se corresponde con un directorio 
        # (esto excluye los posibles ficheros que pudiera contener el 
        # directorio del corpus)
        if os.path.isdir(corpus_path+lan):
            # Si el idioma introducido por el usuario es "ALL", "" o un código
            # de idioma de los que figuran en el corpus
            if lan_to_print == "ALL" or lan_to_print == "" or lan_to_print == lan:
                # Obtenemos los datos de los ficheros train.cupt si existen
                train_data = {}
                if os.path.isfile(corpus_path+lan+"/train.cupt"):
                    train_data = get_data_file(corpus_path+lan+"/train.cupt")
                # Obtenemos los datos de los ficheros dev.cupt si existen
                dev_data = {}
                if os.path.isfile(corpus_path+lan+"/dev.cupt"):
                    dev_data = get_data_file(corpus_path+lan+"/dev.cupt")
                # Obtenemos los datos de los ficheros test.cupt si existen
                test_data = {}
                if os.path.isfile(corpus_path+lan+"/test.cupt"):
                    test_data = get_data_file(corpus_path+lan+"/test.cupt")
                # Obtenemos los datos de los ficheros system.cupt si existen
                system_data = {}
                if os.path.isfile(corpus_path+lan+"/system.cupt"):
                    system_data = get_data_file(corpus_path+lan+"/system.cupt")
                # Añadimos a un diccionario los datos de los train.cupt 
                # correspondientes a todos los idiomas seleccionados 
                all_train_data.update({lan: train_data})
                # Añadimos a un diccionario los datos de los dev.cupt 
                # correspondientes a todos los idiomas seleccionados 
                all_dev_data.update({lan: dev_data})
                # Añadimos a un diccionario los datos de los test.cupt 
                # correspondientes a todos los idiomas seleccionados 
                all_test_data.update({lan: test_data})
                # Añadimos a un diccionario los datos de los system.cupt 
                # correspondientes a todos los idiomas seleccionados 
                all_system_data.update({lan: system_data})
                # Ponemos la bandera a True para indicar que hay datos para 
                # mostrar. De lo contrario se indicará que el usuario 
                # introdujo un código de idioma que no existe en el corpus
                flag = True
    # Si la bandera es True
    if flag:
        # Hacemos la mezcla de todos lo datos incluidos en los train.cupt de
        # todos los idiomas seleccionados
        all_train_merged_data = merge_data(all_train_data)
        # Hacemos la mezcla de todos lo datos incluidos en los dev.cupt de
        # todos los idiomas seleccionados
        all_dev_merged_data = merge_data(all_dev_data)
        # Hacemos la mezcla de todos lo datos incluidos en los test.cupt de
        # todos los idiomas seleccionados
        all_test_merged_data = merge_data(all_test_data)
        # Hacemos la mezcla de todos lo datos incluidos en los system.cupt de
        # todos los idiomas seleccionados
        all_system_merged_data = merge_data(all_system_data)
        # Imprimimos por pantalla todas las tablas de los train.cupt
        print("##################################################################")
        print("STATISTICS FOR train.cupt: " + corpus_path)
        write_data_all(all_train_merged_data)
        print("##################################################################")
        # Imprimimos por pantalla todas las tablas de los dev.cupt
        print("##################################################################")
        print("STATISTICS FOR dev.cupt: " + corpus_path)
        write_data_all(all_dev_merged_data)
        print("##################################################################")
        # Imprimimos por pantalla todas las tablas de los test.cupt
        print("##################################################################")
        print("STATISTICS FOR test.cupt: " + corpus_path)
        write_data_all(all_test_merged_data)
        print("##################################################################")
        # Imprimimos por pantalla todas las tablas de los system.cupt
        print("##################################################################")
        print("STATISTICS FOR system.cupt: " + corpus_path)
        write_data_all(all_system_merged_data)
        print("##################################################################")
    # Si la bandera es False
    else: 
        # Mostramos el error por haber introducido un código de idioma que no 
        # existe en el corpus
        print("WRONG PARAMETER for language, use " + lans + "for a specific language or ALL/<unspecified> for all languages")

"""
Obtiene los datos de un fichero cupt en un diccionario con tres secciones y 
los datos de las tablas correspondientes a cada sección

Entradas: 
    path: Path del del fichero del que se quiere obtener los datos
    
Salidas: 
    data: datos correspondientes al fichero
"""
def get_data_file(path):
    print("****************************************")
    print(path)
    print("****************************************")
    # Inicialización de variables
    data = {}
    section_sentences = {}
    section_tokens = {}
    section_mwes = {}
    # Obtiene los datos del fichero cupt
    texts, sentences = tools.getDataFromCUPT(path)
    # Obtenemos los datos correspondientes a las tablas de oraciones: Los 
    # desgloses por número de tokens y por número de MWEs
    by_num_tokens, by_num_mwes = getSentencesStatistics(sentences)
    # Añadimos los datos a la variable section_sentences
    section_sentences.update({"Num_tok\tNum_sent": by_num_tokens})
    section_sentences.update({"Num_MWEs\tNum_sent": by_num_mwes})
    # Añadimos los datos de oraciones a la variable data
    data.update({"S E N T E N C E S": section_sentences})
    # Obtenemos los datos correspondientes a las tablas de tokens: Los 
    # desgloses por número de caracteres, por número de caracteres de MWEs y 
    # por número de MWEs. También se incluye el número total de tokens y el 
    # número total de tokens que pertenecen a alguna MWE
    by_num_characters, by_num_characters_vocab, by_num_characters_mwe, by_num_mwes, count_tokens, count_tokens_with_mwe = getTokensStatistics(sentences)
    # Añadimos los datos a la variable section_tokens
    section_tokens.update({"Num_chars\tNum_tok": by_num_characters})
    section_tokens.update({"Num_chars_vocab\tNum_tok": by_num_characters_vocab})
    section_tokens.update({"Num_chars_MWE\tNum_tok": by_num_characters_mwe})
    section_tokens.update({"Num_MWEs\tNum_tok": by_num_mwes})
    section_tokens.update({"count_tokens": count_tokens})
    section_tokens.update({"count_tokens_with_mwe": count_tokens_with_mwe})
    # Añadimos los datos de tokens a la variable data
    data.update({"T O K E N S": section_tokens})
    # Obtenemos los datos correspondientes a las tablas de MWEs: Los 
    # desgloses por número de tokens, por etiqueta, por MWEs cruzadas o 
    # anidadas (sin considerar solapamiento), por MWEs cruzadas o 
    # anidadas (sin considerar ningún tipo de solapamiento), por MWEs cruzadas 
    # o anidadas (considerando solapamiento) y por MWEs con tokens compartidos. 
    # También se incluye el número total de MWEs
    by_num_tokens, by_label, by_crossed_nested_no_shared, by_crossed_nested_shared, by_crossed_nested_all, by_shared_token, count_mwes = getMWEStatistics(sentences)
    # Añadimos los datos a la variable section_mwes
    section_mwes.update({"Num_tok\tNum_MWEs": by_num_tokens})
    section_mwes.update({"Label\tNum_MWEs": by_label})
    section_mwes.update({"Cross/Nest(no shared)\tNum_MWEs": by_crossed_nested_no_shared})
    section_mwes.update({"Cross/Nest(shared)\tNum_MWEs": by_crossed_nested_shared})
    section_mwes.update({"Cross/Nest/Chained/LastMatched/FirstMatched/BothMatched/fullyMatched/Equal\tNum_MWEs": by_crossed_nested_all})
    section_mwes.update({"Shared\tNum_MWEs": by_shared_token})
    section_mwes.update({"count_mwes": count_mwes})
    # Añadimos los datos de MWEs a la variable data
    data.update({"M U L T I   W O R D   E X P R E S I O N S": section_mwes})
    
    return data

"""
Realiza el mezclado de las tablas cuando se realizan conteos de varios idiomas. 
Como no todos los idiomas tienen que tener las mismas opciones en la primera 
columna, en el mezclado se hará la unión de las opciones de las primeras 
columnas de cada tabla. Los valores se rellenaran para aquellos idiomas que 
tengan valor para esa opción y se dejará en blanco en caso de que para ese 
idioma no exista valor para esa opción

Entradas: 
    all_data: Diccionario con los datos de cada uno de los idiomas 
              correspondiente a uno de los ficheros (train.cupt, dev.cupt o 
              test.cup)
Salidas: 
    merged_data: datos mezclados
"""
def merge_data(all_data):
    # Inicialización de variables
    merged_data = {}
    merged_section = {}
    merged_byes = {}
    # Obtenemos el código correspondiente al primero de los idiomas
    first_lan = list(all_data.keys())[0]
    # Recorremos todas las secciones (Oraciones, tokens y MWEs)
    for section in all_data.get(first_lan):
        # Inicializamos la variable merged_section
        merged_section = {}
        # Recorremos todas los desgloses de cada sección   
        for by_key in all_data.get(first_lan).get(section).keys():
            # Inicializamos la variable byes_to_merge
            byes_to_merge = {}
            # Recorremos todos los idiomas
            for lan, value in all_data.items():
                # Obtenemos los datos correspondientes a una tabla
                by_data = all_data.get(lan).get(section).get(by_key)
                # Si los datos corresponden a una tabla (dict) y no a un 
                # número total (int)
                if type(by_data) is dict:
                    # Ordenamos el diccionario de la tabla por las claves
                    by_data = dict(sorted(by_data.items()))
                    # Añadimos el diccionario de la tabla a la variable de
                    # tablas a mezclar
                    byes_to_merge.update({lan: by_data})
                # Si los datos corresponden a un número total (int) también
                # se añaden a la variable de tablas a mezclar pero no se 
                # ordenan
                else:
                    byes_to_merge.update({lan: by_data})
            # Mezclamos las tablas de varios idiomas
            merged_byes = merge_byes(byes_to_merge)
            # Añadimos las tablas mezcladas a la variable merged_section
            merged_section.update({by_key: merged_byes})
        # Añadimos los datos mezclados de una sección a la variable merged_data
        merged_data.update({section: merged_section})

    return merged_data

"""
Realiza el mezclado de la misma tabla en varios idiomas. Estas tablas poseen 
dos columnas:
    1.- Primera columna: consta de una serie de opciones dependiendo del 
        tipo de desglose. Por ejemplo, cuando el desglose es por el número
        de tokens, número de MWEs, etc. la opción será un número, cuando 
        el desglose es por etiqueta tendremos LVC.cause, LVC.full, VID, etc., 
        cuando el desglose es por cruzados/anidados tendremos "-", "c", "cc", 
        "cn", "n", etc. y cuando el desglose es por tokens compartidos "-", 
        "1", "1|1", etc.
    2.- Segunda columna: son números correspondientes al conteo de cada una 
        de las opciones de la primera columna
Aunque cada una de las tablas corresponde al mismo desglose, es posible que 
cada idioma tenga distintas opciones en la primera columna. En ese caso, 
habrá idiomas que para una opción tengan valores y para otas no. Por ejemplo, 
estas dos tablas corresponden al desglose cruzados/anidados (sin considerar 
solapamiento) de los idiomas ES y EU:
    
    Cross/Nest(str)    Num_MWEs        Cross/Nest(str)    Num_MWEs
                       ES                                 EU
    -                  748             -                  1726
    n                  2               n                  28
    nn                 1
    TOTAL              751             TOTAL              1754

Ambas tienen valores para "-" y para "n" pero para "nn" sólo existen valores 
en la versión ES. El resultado del mezclado deberá incluir una fila en la 
tabla de EU que tenga como primer elemento "nn" y como segundo "". El 
resultado final de esta función devolverá todas las tablas con el mismo número 
de filas

Entradas: 
    byes: Diccionario con los datos de una de las tablas desglosado por cada 
          uno de los idiomas
Salidas: 
    merged_byes: Diccionario con los datos de una de las tablas desglosado por 
                 cada uno de los idiomas después de añadir filas con valores 
                 vacíos
"""
def merge_byes(byes):
    # Inicialización de variables
    merged_byes = {}
    # Recorremos todos idiomas para obtener los datos de la tabla 
    # correspondiente
    for lan, by in byes.items():
        # Si merged_byes no tiene datos de una tabla para el idioma 
        # correspondiente creamos una tabla vacía para ese idioma
        if merged_byes.get(lan) == None:
            merged_by = {}
        # Si merged_byes no tiene datos de una tabla para el idioma 
        # correspondiente obtenemos los datos de la tabla para ese idioma
        else:
            merged_by = merged_byes.get(lan)
        # Si los datos corresponden a una tabla (dict) y no a un 
        # número total (int)
        if type(by) is dict:
            # Recorremos todos los datos de la tabla
            for key, value in by.items():
                # Añadimos la fila a merged_by
                merged_by.update({key: value})
                # Si no existe la fila en los otros idiomas, la añadimos con 
                # valores vacíos
                addInOthersIfNotExists(lan, key, byes, merged_byes)
                # Añadimos la tabla al resultado (merged_byes)
                merged_byes.update({lan: merged_by})
        # Si los datos corresponden a un número total (int) también
        # se añaden al resultado (merged_byes) pero no se hace nada con ellos
        else:
            merged_byes.update({lan: by})
        
    # Recorremos de nuevo todos idiomas para obtener los datos de la tabla 
    # correspondiente ya mezclada con el fin de ordenar cada tabla
    for lan, merged_by in merged_byes.items():
        # Si los datos corresponden a una tabla (dict) y no a un 
        # número total (int)
        if type(merged_by) is dict:
            # Ordenamos cada tabla mezclada por las opciones de la primera 
            # columna
            merged_by = dict(sorted(merged_by.items()))
            merged_byes.update({lan: merged_by})
    # Ordenamos el merged_byes por idioma
    merged_byes = dict(sorted(merged_byes.items()))

    return merged_byes

"""
Añade la clave y un valor vacío ("") si el key que se pasa por parámetro no 
existe en la tabla de los otros idiomas

Entradas: 
    lan: Idioma de la tabla del parámetro a añadir en caso de que no exista
    key: Clave (primer elemento) de la fila a añadir
    byes: Diccionario con los datos de una de las tablas desglosado por cada 
          uno de los idiomas
    merged_byes: Diccionario con los datos de una de las tablas desglosado por 
                 cada uno de los idiomas después de añadir filas con valores 
                 vacíos
Salidas: 
    merged_byes: Diccionario con los datos de una de las tablas desglosado por 
                 cada uno de los idiomas después de añadir filas con valores 
                 vacíos
"""
def addInOthersIfNotExists(lan, key, byes, merged_byes):
    # Recorremos todas las tablas para cada idioma
    for lan2, by in byes.items():
        # Actualizamos las tablas de todos los idiomas excepto las del idioma 
        # pasado por parámetro
        if lan != lan2:
            # Si la fila no existe en las tablas de otros idiomas
            if(byes.get(lan2).get(key) == None):
                # Si la tabla no existe para el idioma en la lista de tablas 
                # mezcladas
                if merged_byes.get(lan2) == None:
                    # Creamos la tabla
                    merged_by = {}
                    # Añadimos la fila con la clave pasada por parámetro y el 
                    # valor vacío ("")
                    merged_by.update({key:"0"})
                    # Añadimos la nueva tabla a la lista de tablas mezcladas
                    merged_byes.update({lan2: merged_by})
                # Si la tabla existe para el idioma en la lista de tablas 
                # mezcladas
                else:
                    # Añadimos la fila con la clave pasada por parámetro y el 
                    # valor vacío ("")
                    merged_byes.get(lan2).update({key:"0"})

"""
Muestra por pantalla toda la información correspondiente a un fichero cupt 
(train.cupt, dev.cupt o test.cupt) desglosada por seccion y por tabla. La 
tabla tendrá una primera columna con las claves y tantas columnas de valores 
como idiomas se hayan seleccionado por el usuario.

NOTA: Esta función es complementaria a la siguiente y pueden utilizarse 
alternativamente una u otra. Sólo son dos formas distintas de mostrar los 
resultados. Para cambiar de una a otra sólo hay que cambiarle el nombre a la 
función. Se ejecutará siempre la que tenga el nombre "write_data_all". Le 
cambiaremos el nombre a la otra para conservarla.

Entradas: 
    data: Diccionario con los datos correspondientes a un fichero cupt
Salidas: 
    void: Muestra por pantalla la información contenida en el diccionario 
          pasado por parámetro
"""
def write_data_all_old(data):
    # Inicialización de variables. Utilizaremos un diccionario de contadores 
    # para poder mostrar al final de la tabla los totales de cada idioma
    counters = {}
    # Recorremos todas las secciones de los datos (oraciones, tokens y MWEs)
    for section, byes in data.items():
        # Mostramos el nombre de la sección
        print("\n" + section)
        # Recorremos cada tabla
        for by_key, by in byes.items():
            # Inicializamos el texto de la tabla para mostrar
            table = ""
            # Inicializamos el diccionario de contadores de cada idioma
            counters = {}
            # Como el diccionario de tablas viene desglosado por idiomas, hay 
            # que reordenar la información de forma que la primera columna 
            # corresponda a las claves de las tablas ya mezcladas (es decir, 
            # con valores vacíos donde corresponda. Tras haber mezclado 
            # las tablas, todas ellas tendrán el mismo número de filas), tras 
            # el cambio de filas por columnas cada fila será una de las claves 
            # de la tabla y cada columna correspondera a los valores 
            # correspondientes a un idioma
            by_change_rows_columns = change_rows_columns(by)
            for key, by_data in by_change_rows_columns.items():
                # Inicializamos el texto de la fila para mostrar
                row = ""
                # Inicializamos el texto de la fila cabecera que muestra los 
                # idiomas
                lans = ""
                # Si los datos corresponden a una tabla (dict) y no a un 
                # número total (int)
                if type(by_data) is dict:
                    # Recorremos todos los idiomas y sus correspondientes 
                    # valores
                    for lan, value in by_data.items():
                        # Acumulamos los idiomas en la variable lans 
                        # separándolos por un tabulador
                        lans = lans + "\t" + lan
                        # Para actualizar los contadores, si nos encontramos 
                        # un valor vacío lo transformamos en 0, si no es vacío
                        # usaremos el valor encontrado
                        if value == "":
                            new_value = 0
                        else:
                            new_value = value
                        # Si el texto de la fila es vacío estamos al 
                        # principio de una fila. 
                        if row == "":
                            # Añadimos a la fila el campo y el valor 
                            # correspondiente al primero de los idiomas
                            row = row + str(key) + "\t" + str(value)
                            # Para actualizar los contadores si en el 
                            # diccionario counters todavía no hay información
                            # para el idioma
                            if counters.get(lan) is None:
                                # Creamos la información para el idioma con el 
                                # nuevo valor
                                counters.update({lan: new_value})
                            # Para actualizar los contadores si en el 
                            # diccionario counters ya hay información para el 
                            # idioma
                            else:
                                # Actualizamos la información sumando el nuevo 
                                # valor al valor acumulado previamente
                                counters.update({lan: int(counters.get(lan))+int(new_value)})
                        # Si el texto de la línea no es vacío no estamos al 
                        # principio de una línea. 
                        else:
                            # Añadimos a la fila y el valor correspondiente al 
                            # idioma separándolo por un tabulador
                            row = row + "\t" + str(value)
                            # Para actualizar los contadores si en el 
                            # diccionario counters todavía no hay información
                            # para el idioma
                            if counters.get(lan) is None:
                                # Creamos la información para el idioma con el 
                                # nuevo valor
                                counters.update({lan: new_value})
                            # Para actualizar los contadores si en el 
                            # diccionario counters ya hay información para el 
                            # idioma
                            else:
                                # Actualizamos la información sumando el nuevo 
                                # valor al valor acumulado previamente
                                counters.update({lan: int(counters.get(lan))+int(new_value)})
                # Si los datos corresponden a un número total (int) 
                else:
                    # Como no se trata de una tabla sino sólo de un valor, 
                    # sólo vamos a imprimir la clave ("count_tokens", 
                    # "count_mwes", ...) seguida del valor separada por una 
                    # tabulación. Esta información no se añade ni a una fila 
                    # (row) ni a la tabla
                    by_key = by_key + "\t" + str(by_data)
                # Añadimos la fila a la tabla
                table = table + row + "\n"
            # Generamos una última fila con los totales, que son los valores 
            # finales de la variable counters
            row = "TOTAL"
            # Recorremos todos los totales de cada idioma
            for value in counters.values():
                # Añadimos cada total a la fila separado por una tabulación
                row = row + "\t" + str(value)
            # Añadimos esta última fila a la tabla
            table = table + row + "\n"
            # Si la fila generada no es igual a la cadena "TOTAL", entonces se 
            # trata de una tabla, por lo que imprimiremos el encabezamiento 
            # que será una fila con los nombres de campos correspondientes a 
            # la primera columna y el resto de columnas de idiomas, una 
            # segunda fila con la lista de idiomas separados por tabulaciones
            # y la tabla generada en el proceso anterior
            if (row != "TOTAL"):
                print(by_key + "\n" + lans + "\n" + table)
            # Si la fila generada es igual a la cadena "TOTAL", entonces no se 
            # han añadido los totales porque el by_data no era una tabla sino 
            # un entero por lo que imprimimos by_key [la clave ("count_tokens", 
            # "count_mwes", ...) seguida del valor separada por una 
            # tabulación]
            else:
                print(by_key)

"""
Muestra por pantalla toda la información correspondiente a un fichero cupt 
(train.cupt, dev.cupt o test.cupt) desglosada por seccion y por tabla. La 
tabla tendrá una primera columna con los idiomas y tantas columnas de valores 
como claves se hayan seleccionado por el usuario. 

NOTA: Esta función es complementaria a la anterior y pueden utilizarse 
alternativamente una u otra. Sólo son dos formas distintas de mostrar los 
resultados. Para cambiar de una a otra sólo hay que cambiarle el nombre a la 
función. Se ejecutará siempre la que tenga el nombre "write_data_all". Le 
cambiaremos el nombre a la otra para conservarla.

Entradas: 
    data: Diccionario con los datos correspondientes a un fichero cupt
Salidas: 
    void: Muestra por pantalla la información contenida en el diccionario 
          pasado por parámetro
"""
def write_data_all(data):
    # Recorremos todas las secciones de los datos (oraciones, tokens y MWEs)
    for section, byes in data.items():
        # Mostramos el nombre de la sección
        print("\n" + section)
        # Recorremos cada tabla
        for by_key, by in byes.items():
            # Mostramos by_key
            print("\t" + by_key)
            # Obtenemos los idiomas
            lans = list(by.keys())
            # Si no es una tabla de totales (count_mwes, count_tokens, etc.)
            # entonces es una tabla normal
            if not isinstance(by.get(lans[0]), int):
                # Obtenemos las claves de los datos del primer idioma (primera 
                # fila de la tabla)
                first_row_data = list(by.get(lans[0]).keys())
                # Inicializamos el string de la primera fila
                first_row = ""
                # Recorremos todas las claves
                for item in first_row_data:
                    # Concatenamos las claves separadas por tabulación
                    first_row = first_row + "\t" + str(item)
                # Mostramos la primera fila
                print (first_row + "\t TOTAL")
                # Recorremos los idiomas
                for lan in lans:
                    # Obtenemos los datos para cada idioma
                    row_data = list(by.get(lan).values())
                    # Inicializamos fila con el código de idioma
                    row = lan
                    # Inicializamos el sumador de los datos del idioma
                    total = 0
                    # Recorremos los datos
                    for item in row_data:
                        # Concatemamos los datos seprardos por tabulación
                        row = row + "\t" + str(item)
                        # Sumamos los datos del idioma
                        total = total + int(item)
                    # Mostramos la fila de datos correspondiente al idioma y
                    # concatenada a la cifra total después de sumar todos los 
                    # datos
                    print(row + "\t" + str(total))
            # Si es una tabla de totales (count_mwes, count_tokens, etc.)
            # entonces desglosamos los valores totales para cada idioma
            else:
                for lan in lans:
                    row = lan + "\t" + str(by.get(lan))
                    print(row)
            print()
"""
            # Recorremos todos los idiomas
            for key, by_data in by.items():
                print("********")
                print(key)
                print(by_data)
                # Inicializamos el texto de la fila para mostrar
                row = ""
                # Inicializamos el texto de la fila cabecera que muestra los 
                # idiomas
                lans = ""
                # Si los datos corresponden a una tabla (dict) y no a un 
                # número total (int)
                if type(by_data) is dict:
                    # Recorremos todos los idiomas y sus correspondientes 
                    # valores
                    for lan, value in by_data.items():
                        # Acumulamos los idiomas en la variable lans 
                        # separándolos por un tabulador
                        lans = lans + "\t" + lan
                        # Para actualizar los contadores, si nos encontramos 
                        # un valor vacío lo transformamos en 0, si no es vacío
                        # usaremos el valor encontrado
                        if value == "":
                            new_value = 0
                        else:
                            new_value = value
                        # Si el texto de la fila es vacío estamos al 
                        # principio de una fila. 
                        if row == "":
                            # Añadimos a la fila el campo y el valor 
                            # correspondiente al primero de los idiomas
                            row = row + str(key) + "\t" + str(value)
                            # Para actualizar los contadores si en el 
                            # diccionario counters todavía no hay información
                            # para el idioma
                            if counters.get(lan) is None:
                                # Creamos la información para el idioma con el 
                                # nuevo valor
                                counters.update({lan: new_value})
                            # Para actualizar los contadores si en el 
                            # diccionario counters ya hay información para el 
                            # idioma
                            else:
                                # Actualizamos la información sumando el nuevo 
                                # valor al valor acumulado previamente
                                counters.update({lan: int(counters.get(lan))+int(new_value)})
                        # Si el texto de la línea no es vacío no estamos al 
                        # principio de una línea. 
                        else:
                            # Añadimos a la fila y el valor correspondiente al 
                            # idioma separándolo por un tabulador
                            row = row + "\t" + str(value)
                            # Para actualizar los contadores si en el 
                            # diccionario counters todavía no hay información
                            # para el idioma
                            if counters.get(lan) is None:
                                # Creamos la información para el idioma con el 
                                # nuevo valor
                                counters.update({lan: new_value})
                            # Para actualizar los contadores si en el 
                            # diccionario counters ya hay información para el 
                            # idioma
                            else:
                                # Actualizamos la información sumando el nuevo 
                                # valor al valor acumulado previamente
                                counters.update({lan: int(counters.get(lan))+int(new_value)})
                # Si los datos corresponden a un número total (int) 
                else:
                    # Como no se trata de una tabla sino sólo de un valor, 
                    # sólo vamos a imprimir la clave ("count_tokens", 
                    # "count_mwes", ...) seguida del valor separada por una 
                    # tabulación. Esta información no se añade ni a una fila 
                    # (row) ni a la tabla
                    by_key = by_key + "\t" + str(by_data)
                # Añadimos la fila a la tabla
                table = table + row + "\n"
            # Generamos una última fila con los totales, que son los valores 
            # finales de la variable counters
            row = "TOTAL"
            # Recorremos todos los totales de cada idioma
            for value in counters.values():
                # Añadimos cada total a la fila separado por una tabulación
                row = row + "\t" + str(value)
            # Añadimos esta última fila a la tabla
            table = table + row + "\n"
            # Si la fila generada no es igual a la cadena "TOTAL", entonces se 
            # trata de una tabla, por lo que imprimiremos el encabezamiento 
            # que será una fila con los nombres de campos correspondientes a 
            # la primera columna y el resto de columnas de idiomas, una 
            # segunda fila con la lista de idiomas separados por tabulaciones
            # y la tabla generada en el proceso anterior
            if (row != "TOTAL"):
                print(by_key + "\n" + lans + "\n" + table)
            # Si la fila generada es igual a la cadena "TOTAL", entonces no se 
            # han añadido los totales porque el by_data no era una tabla sino 
            # un entero por lo que imprimimos by_key [la clave ("count_tokens", 
            # "count_mwes", ...) seguida del valor separada por una 
            # tabulación]
            else:
                print(by_key)
"""

"""
El diccionario cada tabla viene desglosado por idiomas y después por las filas 
de cada tabla. Pero para mostrarlo en pantalla queremos que se muestre en cada 
fila las claves que están en la primera posición de la fila y los valores de 
cada uno de los idiomas. Por este motivo, debemos reordenar la información
de forma que la primera columna corresponda a las claves de las tablas ya 
mezcladas. Tras el cambio de filas por columnas cada fila comenzará con una 
de las claves de la tabla y cada columna a partir de la segunda correspondera 
a los valores de un idioma

Entradas: 
    by: Tablas originales desglosadas por idiomas
Salidas: 
    result: Tablas desglosadas por la clave de la tabla que incluyen en una 
            fila los valores correspondientes a cada idioma
"""
def change_rows_columns(by):
    # Inicialización de variables
    result = {}
    # Obtenemos el código del primer idioma
    first_lan = list(by.keys())[0]
    # Si los datos del primer idioma corresponden a una tabla (dict) y no a 
    # un número total (int)
    if type(by.get(first_lan)) is dict:
        # Recorremos todas las filas de la tabla
        for key, value in by.get(first_lan).items():
            # Inicializamos la variable valores que es un diccionario donde se 
            # almacenarán los valores de cada idioma correspondientes a la 
            # clave
            values = {}
            # Recorremos todos los idiomas
            for lan in by.keys():
                # metemos los valores de cada idioma en la variable values
                values.update({lan: by.get(lan).get(key)})
                # Asociamos a la clave el diccionario values que tiene los 
                # valores de cada idioma
                result.update({key: values})
    # Si los datos corresponden a un número total (int) no se hace ningún tipo 
    # de reordenamiento
    else:
        # El dato correspondiente se almacena en el resultado
        result = by
    return result

"""
Obtiene los conteos de la sección de oraciones correspondiente a un fichero 
cupt. Serán 2 tablas con los siguientes desgloses:
    POR NÚMERO DE TOKENS: Número de oraciones desglosado por número de tokens 
                          de la oración. Por ejemplo, el corpus EU tiene 4 
                          oraciones con 2 tokens, 44 oraciones con 3 tokens, 
                          91 oraciones con 4 tokens, ...:
                
                            Num_tok	   	Num_sent
                                    	EU
                            2   	   	   	4
                            3   	   	   	44
                            4   	   	   	91
                            ...
                
    POR NÚMERO DE MWEs: Número de oraciones desglosado por número de MWEs de la 
                        oración. Por ejemplo, el corpus EU tiene 3257 oraciones 
                        con 0 MWEs, 1157 oraciones con 1 MWE, 225 oraciones con 
                        2 MWEs, ...:
                
                            Num_MWEs	Num_sent
                                	   	   	EU
                            0   	   	   	3257
                            1   	   	   	1157
                            2   	   	   	225
                            3   	   	   	35
                            4   	   	   	8
                            5   	   	   	2
                            TOTAL	   	4684

Entradas: 
    sentences: Lista de oraciones obtenida de la función getDataFromCUPT() del 
               paquete tools
Salidas: 
    by_num_tokens: Datos de la tabla de número de oraciones desglosada por 
                   número de tokens que contiene la oración
    by_num_mwes: Datos de la tabla de número de oraciones desglosada por 
                 número de MWEs que contiene la oración
"""
def getSentencesStatistics(sentences):
    # Inicialización de variables
    by_num_tokens = {}
    by_num_mwes = {}
    # Recorremos todas las oraciones
    for id, sentence in enumerate(sentences):
        # Obtenemos el número de tokens de la oración que es el númeo de 
        # elementos que tiene la lista que contiene la información de esa 
        # oración
        num_tokens = len(sentence)
        # Buscamos en la tabla por número de tokens si ya hay contabilizadas 
        # oraciones con ese número de tokens
        sentences_with_this_num_tokens = by_num_tokens.get(num_tokens)
        # Si no hay contabilizadas oraciones con ese número de tokens, la 
        # búsqueda anterior devolverá "None"
        if sentences_with_this_num_tokens == None:
            # En ese caso el número de oraciones con ese número de tokens 
            # será 1
            sentences_with_this_num_tokens = 1
        # Si hay contabilizadas oraciones con ese número de tokens, la 
        # búsqueda devolverá un número
        else:
            # Sumamos 1 al número de oraciones con ese número de tokens
            sentences_with_this_num_tokens = sentences_with_this_num_tokens + 1
        # Actualizamos la tabla con el nuevo valor para ese número de tokens
        by_num_tokens.update({num_tokens: sentences_with_this_num_tokens})
        # Obtenemos el número de MWEs de la oración que es el númeo de 
        # elementos que tiene el diccionario que contiene las MWEs de esa 
        # oración
        num_mwes = len(getMWEs(sentence, id)[0])
        # Buscamos en la tabla por número de MWEs si ya hay contabilizadas 
        # oraciones con ese número de MWEs
        sentences_with_this_num_mwes = by_num_mwes.get(num_mwes)
        # Si no hay contabilizadas oraciones con ese número de MWEs, la 
        # búsqueda anterior devolverá "None"
        if sentences_with_this_num_mwes == None:
            # En ese caso el número de oraciones con ese número de MWEs 
            # será 1
            sentences_with_this_num_mwes = 1
        # Si hay contabilizadas oraciones con ese número de MWEs, la 
        # búsqueda devolverá un número
        else:
            # Sumamos 1 al número de oraciones con ese número de MWEs
            sentences_with_this_num_mwes = sentences_with_this_num_mwes + 1
        # Actualizamos la tabla con el nuevo valor para ese número de MWEs
        by_num_mwes.update({num_mwes: sentences_with_this_num_mwes})
        
    return by_num_tokens, by_num_mwes

"""
Obtiene 4 diccionarios correspondientes a una oración:
    
    1.- Diccionario con las MWEs que contiene la oración. El formato del 
        diccionario es este:
            clave = string con este formato que identifica una MWE:

<indice_de_la_oración_en_la_lista_sentences>-<indice_de_MWE_según_se_indica_en_el_cupt>

            valor = lista con el siguiente formato

[<etiqueta_de_la_MWE>, <indice_del_primer_token_de_la_MWE>, <indice_del_segundo_token_de_la_MWE>, ...]

    2.- Diccionario con las MWEs cruzadas/anidadas (sin considerar 
        solapamiento en los extremos) que contiene la oración. El formato del diccionario es 
        este:
            clave = string con este formato que identifica una MWE:

<indice_de_la_oración_en_la_lista_sentences>-<indice_de_MWE_según_se_indica_en_el_cupt>

            valor = string de "c" y "n" repetidas tantas veces como cruces (c) 
                    o anidamientos (n) tenga la MWE con las otras de la 
                    oración. Por ejemplo "cnn" significa que la MWE se cruza 
                    con otra y se anida con dos
    
    3.- Diccionario con las MWEs cruzadas/anidadas (sin considerar ningún tipo
        de solapamiento) que contiene la oración. El formato del diccionario es 
        el mismo que el del diccionario del apartado anterior
    
    4.- Diccionario con las MWEs cruzadas/anidadas (considerando 
        solapamiento) que contiene la oración. El formato del diccionario es 
        el mismo que el del diccionario del apartado anterior
    
    5.- Diccionario con las MWEs que comparten tokens con otras de la oración. 
        El formato del diccionario es este:
            clave = string con este formato que identifica una MWE:

<indice_de_la_oración_en_la_lista_sentences>-<indice_de_MWE_según_se_indica_en_el_cupt>

            valor = string con el formato <número>|<número>| ... |<número> que 
                    indica el número de tokens compartidos y el número de MWEs 
                    con las que se comparten. Por ejemplo, 2|2|1 significa que 
                    la MWE comparte tokens con otras 3 MWEs: 2 con una de 
                    ellas, 2 con otra y 1 con otra

Entradas: 
    sentence: Lista de tokens con información sobre una oración
    id_sent: Índice de la oración en la lista de oraciones (se utilizará para 
             crear la clave que identifica la MWE)
Salidas: 
    mwes: Diccionario de MWEs descrito en 1
    getCrossedNested(mwes, "str", sentence): Diccionario de MWEs descrito en 2
    getCrossedNested(mwes, "str_none", sentence): Diccionario de MWEs descrito en 3
    getCrossedNested(mwes, "ovl", sentence): Diccionario de MWEs descrito en 4
    getShared(mwes): Diccionario de MWEs descrito en 5
"""
def getMWEs(sentence, id_sent):
    # Inicialización de variables
    mwes = {}
    # Recorremos los tokens de la oración
    for id, token in enumerate(sentence):
        # Si la información del token relativa a MWEs (indice 10) es distinta 
        # de "*" (es decir, si el token pertenece a una MWE)
        if token[10] != "*":
            # Hacemos el split ";" del token por si estuviese asociado a 
            # varias MWEs
            token_mwes = token[10].split(";")
            # Recorremos todas las cadenas tras el split (si no hay ; sólo 
            # habrá una cadena)
            for mwe in token_mwes:
                # Si es el primer token de la MWE entonces tendrá formato 
                # <número_de_MWE_en_la_oracion>:<etiqueta>, por tanto, 
                # separamos ambos datos
                num_label = mwe.split(":")
                # Si es el primer token de la MWE tras el split tendremos dos 
                # strings
                if len(num_label) == 2:
                    # Añadimos la nueva MWE a mwes construyendo la clave y 
                    # poniendo como valor la lista cuyo primer elemento es la 
                    # etiqueta de la MWE y el segundo el índice del primer 
                    # token de la MWE
                    mwes.update({str(id_sent) + "-" + num_label[0]: [num_label[1], id]})
                # Si no es el primer token de la MWE, tras el split tendremos 
                # un sólo string. En este caso la MWE ya estará incluida en el 
                # diccionario resultante
                if len(num_label) == 1:
                    # Obtenemos la lista [etiqueta, indice1, ...]
                    list_label_indexes = mwes.get(str(id_sent) + "-" + num_label[0])
                    # Añadimos el índice del token a la lista de índices de 
                    # tokens donde aparece la MWE
                    list_label_indexes.append(id)
                    # Actualizamos mwes con la nueva lista de índices de tokens
                    mwes.update({str(id_sent) + "-" + num_label[0]: list_label_indexes})
    
    return mwes, getCrossedNested(mwes, "c_n_no_shared", sentence), getCrossedNested(mwes, "c_n_shared", sentence), getCrossedNested(mwes, "all", sentence), getShared(mwes)

"""
Obtiene los conteos de la sección de tokens correspondiente a un fichero 
cupt. Serán 3 tablas con los siguientes desgloses y dos números:
    TABLA POR NÚMERO DE CARACTERES DEL TOKEN: Número de tokens desglosado por 
                número de caracteres del texto del token. Por ejemplo, el 
                corpus EU tiene 10695 tokens con 1 caracter, 2975 tokens 
                con 2 caracters, 5569 tokens con 3 caracters, ...:
                    
                    Num_chars	Num_tok
                    	   	   	   	EU
                    1	   	   	   	10695
                    2	   	   	   	2975
                    3	   	   	   	5569
                    ...
    
    TABLA POR NÚMERO DE CARACTERES DEL TOKEN: Esta tabla es idéntica a la 
                anterior pero en este caso se genera un vocabulario del 
                corpus, de tal forma que si un token aparece varias veces, 
                sólo se cuenta una vez. Esto evita que artículos, 
                preposiciones, signos de puntuación etc. cuya frecuencia es
                alta en los textos hagan disminuir la media del tamaño de 
                los tokens.
            
    TABLA POR NÚMERO DE CARACTERES DE LA ETIQUETA DE LA MWE: Número de tokens 
                con información sobre MWEs (se excluyen de la cuenta los tokens 
                que tienen "*") desglosado por el número de caracteres de la 
                etiqueta MWE del token. Por ejemplo, el corpus EU tiene 1757 
                tokens con 1 caracter en su etiqueta MWE, 11 tokens con 3 
                caracteres en su etiqueta MWE, 357 tokens con 5 caracteres en 
                su etiqueta MWE, ...:
                    
                    Num_chars_MWE	Num_tok
                    	   	   	   	   	EU
                    1	   	   	   	   	1757
                    3	   	   	   	   	11
                    5	   	   	   	   	357
                    ...

    TABLA POR EL NÚMERO DE MWEs A LAS QUE PERTENECE EL TOKEN: Número de tokens 
                desglosado por número de MWEs a las que pertenece el token. 
                Por ejemplo, el corpus EU tiene 63313 tokens que no pertenecen 
                a ninguna MWE, 3499 tokens que pertenecen a 1 MWE y 21 tokens 
                que pertenecen a 2 MWEs:
                    
                    Num_MWEs	Num_tok
                    	   	   	   	EU
                    0	   	   	   	63313
                    1	   	   	   	3499
                    2	   	   	   	21
                    TOTAL	   	66833
    
    NÚMERO TOTAL DE TOKENS
    
    NÚMERO TOTAL DE TOKENS QUE PERTENECEN A AL MENOS UNA MWE

Entradas: 
    sentences: Lista de oraciones obtenida de la función getDataFromCUPT() del 
               paquete tools
Salidas:
    by_num_characters: Datos de la tabla de número de tokens desglosada por 
                       número de caracteres del texto del token
    by_num_characters_mwe: Datos de la tabla de número de tokens desglosada 
                           por número de caracteres del texto de la etiqueta
    by_num_mwes: Datos de la tabla de número de tokens desglosada por número 
                 de MWEs a las que pertenece el token
    count_tokens: Número total de tokens
    count_tokens_with_mwe: Número total de tokens que pertencen a al menos 
                           una MWE
"""

def getTokensStatistics(sentences):
    # Inicialización de variables
    by_num_characters = {}
    by_num_characters_vocab = {}
    vocab = []
    by_num_characters_mwe = {}
    by_num_mwes = {}
    count_tokens = 0
    count_tokens_with_mwe = 0
    # Recorremos todas las oraciones
    for sentence in sentences:
        # Recorremos todos los tokens de cada oración
        for token in sentence:
            # Sumamos 1 al contador de tokens
            count_tokens = count_tokens + 1
            # Obtenemos el número de caracteres del texto del token
            num_characters = len(token[1])
            # Buscamos en la tabla por número de caracteres si ya hay 
            # contabilizados tokens con ese número de caracteres
            tokens_with_this_num_characters = by_num_characters.get(num_characters)
            # Si no hay contabilizados tokens con ese número de caracteres, la 
            # búsqueda anterior devolverá "None"
            if tokens_with_this_num_characters == None:
                # En ese caso el número de tokens con ese número de caracteres 
                # será 1
                tokens_with_this_num_characters = 1
            # Si hay contabilizados tokens con ese número de caracteres, la 
            # búsqueda anterior devolverá un número
            else:
                # Sumamos 1 al número de tokens con ese número de caracteres
                tokens_with_this_num_characters = tokens_with_this_num_characters + 1
            # Actualizamos la tabla con el nuevo valor para ese número de 
            # caracteres
            by_num_characters.update({num_characters: tokens_with_this_num_characters})
            # Si el texto del token está en el vocabulario se contabilizará. 
            if token[1] not in vocab:
                # Obtenemos el número de caracteres del texto del token
                num_characters = len(token[1])
                # Buscamos en la tabla por número de caracteres si ya hay 
                # contabilizados tokens con ese número de caracteres
                tokens_with_this_num_characters_vocab = by_num_characters_vocab.get(num_characters)
                # Si no hay contabilizados tokens con ese número de caracteres, la 
                # búsqueda anterior devolverá "None"
                if tokens_with_this_num_characters_vocab == None:
                    # En ese caso el número de tokens con ese número de caracteres 
                    # será 1
                    tokens_with_this_num_characters_vocab = 1
                # Si hay contabilizados tokens con ese número de caracteres, la 
                # búsqueda anterior devolverá un número
                else:
                    # Sumamos 1 al número de tokens con ese número de caracteres
                    tokens_with_this_num_characters_vocab = tokens_with_this_num_characters_vocab + 1
                # Actualizamos la tabla con el nuevo valor para ese número de 
                # caracteres
                by_num_characters_vocab.update({num_characters: tokens_with_this_num_characters_vocab})
                # Añadimos el texto del token al vocabulario para que no se 
                # vuelva a contabilizar
                vocab.append(token[1])
            # Si la información del token relativa a MWEs (indice 10) es 
            # distinta de "*" (es decir, si el token pertenece a una MWE)
            if token[10] != "*":
                # Sumamos 1 al contador de tokens que pertenecen al menos a 
                # una MWE
                count_tokens_with_mwe = count_tokens_with_mwe + 1
                # Obtenemos el número de caracteres de la información de MWEs
                num_characters_mwe = len(token[10])
                # Buscamos en la tabla por número de caracteres de MWE si ya 
                # hay contabilizados tokens con ese número de caracteres
                tokens_with_this_num_characters_mwe = by_num_characters_mwe.get(num_characters_mwe)
                # Si no hay contabilizados tokens con ese número de caracteres 
                # en la MWE, la búsqueda anterior devolverá "None"
                if tokens_with_this_num_characters_mwe == None:
                    # En ese caso el número de tokens con ese número de 
                    # caracteres en la MWE será 1
                    tokens_with_this_num_characters_mwe = 1
                # Si hay contabilizados tokens con ese número de caracteres en 
                # la MWE, la búsqueda anterior devolverá un número
                else:
                    # Sumamos 1 al número de tokens con ese número de 
                    # caracteres en la MWE
                    tokens_with_this_num_characters_mwe = tokens_with_this_num_characters_mwe + 1
                # Actualizamos la tabla con el nuevo valor para ese número de 
                # caracteres de MWE
                by_num_characters_mwe.update({num_characters_mwe: tokens_with_this_num_characters_mwe})
            # Obtenemos el número de MWEs a las que pertenece el token
            num_mwes = getMWEsToken(token)
            # Buscamos en la tabla por número de MWEs si ya hay contabilizados 
            # tokens con ese número de MWEs a las que pertenecen
            tokens_with_this_num_mwes = by_num_mwes.get(num_mwes)
            # Si no hay contabilizados tokens con ese número de MWEs, la 
            # búsqueda anterior devolverá "None"
            if tokens_with_this_num_mwes == None:
                # En ese caso el número de tokens con ese número de MWEs
                # será 1
                tokens_with_this_num_mwes = 1
            # Si hay contabilizados tokens con ese número de MWEs, la 
            # búsqueda anterior devolverá un número
            else:
                # Sumamos 1 al número de tokens con ese número de MWEs
                tokens_with_this_num_mwes = tokens_with_this_num_mwes + 1
            # Actualizamos la tabla con el nuevo valor para ese número de MWEs
            by_num_mwes.update({num_mwes: tokens_with_this_num_mwes})
    
    return by_num_characters, by_num_characters_vocab, by_num_characters_mwe, by_num_mwes, count_tokens, count_tokens_with_mwe

"""
Obtiene el número de MWEs a las que pertenece el token que se le pasa por 
parámetro

Entradas: 
    token: Lista de items con la información de un token
Salidas:
    result: Número de MWEs a las que pertenece el token
"""
def getMWEsToken(token):
    # Inicialización de variables
    result = 0
    # Si la información del token relativa a MWEs (indice 10) es 
    # distinta de "*" (es decir, si el token pertenece a una MWE)
    if token[10] != "*":
        # El resultado será el número de elementos que contiene la lista 
        # resultante de hacer split(";") sobre la información relateiva a 
        # MWEs (indice 10)
        result = len(token[10].split(";"))
    return result

"""
Obtiene los conteos de la sección de MWEs correspondiente a un fichero 
cupt. Serán 5 tablas con los siguientes desgloses y un número:
    
    TABLA POR NÚMERO DE TOKENS DE LA MWE: Número de MWEs desglosado por número 
            de tokens que tiene la MWE. Por ejemplo, el corpus EU tiene 
            1724 MWEs de 2 tokens, 27 MWEs de 3 tokens y 3 MWEs de 4 tokens:
                
                Num_tok	Num_MWEs
                	   	   	EU
                2	   	   	1724
                3	   	   	27
                4	   	   	3
                TOTAL	1754
                
    TABLA POR TIPO DE ETIQUETA: Número de MWEs desglosado por el tipo de 
            etiqueta que tiene la MWE. Por ejemplo, el corpus EU tiene 92 MWEs 
            LVC.cause, 1304 MWEs LVC.full y 358 MWEs VID:
                
                Label	   	Num_MWEs
                	   	   	   	EU
                LVC.cause	92
                LVC.full	1304
                VID	   	   	358
                TOTAL	   	1754
    
    TABLA POR CRUZADA/ANIDADA (SIN SOLAPAMIENTO EN LOS EXTREMOS): Número de 
            MWEs desglosado por el tipo de MWE según si es cruzada o anidada 
            (sin considerar solapamiento en los extremos). 
            
            Sean dos MWEs A = [t_1, ...t_n] y B = [s_1, ...s_m], donde 
            los t_i son las posiciones de los tokens de la MWE A y los 
            s_i las posiciones de los tokens de la MWE B:
            
            * CRUZADAS: En este apartado se considera que A y B están 
              cruzadas (sin considerar solapamiento) ssi:
                  t_1 < s_1 and s_1 < t_n and t_n < s_m
            * ANIDADAS: En este apartado se considera que A y B están 
              anidadas (sin considerar solapamiento) ssi:
                  t_1 < s_1 and s_1 < s_m and s_m < t_n
            
            Por ejemplo, considerando las definiciones anteriores el 
            corpus ES tiene 1724 MWEs ni cruzadas ni anidadas, 6 MWEs 
            cruzadas y 2 MWEs anidadas:
                
                Cross/Nest(str)	Num_MWEs
                	                ES
                -	            1724
                c	            6
                n	            2
                TOTAL	        1732
                
    TABLA POR CRUZADA/ANIDADA (SIN NINGÚN TIPO DE SOLAPAMIENTO): Número de 
            MWEs desglosado por el tipo de MWE según si es cruzada o anidada 
            (sin considerar ningún tipo de solapamiento). 
            
            Sean dos MWEs A = [t_1, ...t_n] y B = [s_1, ...s_m], donde 
            los t_i son las posiciones de los tokens de la MWE A y los 
            s_i las posiciones de los tokens de la MWE B:
            
            * CRUZADAS: En este apartado se considera que A y B están 
              cruzadas (sin considerar ningún tipo de solapamiento) ssi:
                  t_1 < s_1 and s_1 < t_n and t_n < s_m  
                  and A intersección B = 0
            * ANIDADAS: En este apartado se considera que A y B están 
              anidadas (sin considerar solapamiento) ssi:
                  t_1 < s_1 and s_1 < s_m and s_m < t_n
                  and A intersección B = 0
            
            Por ejemplo, considerando las definiciones anteriores el 
            corpus HR tiene 1329 MWEs ni cruzadas ni anidadas, 2 MWEs 
            anidadas y 1 MWE doblemente anidada:
                
                Cross/Nest(none)	Num_MWEs
                                 HR
                -	            1329
                n	            2
                nn	            1
                TOTAL           1332
    
    TABLA POR CRUZADA/ANIDADA (CON SOLAPAMIENTO): Número de MWEs desglosado 
            por el tipo de MWE según si es cruzada o anidada (considerando 
            solapamiento). 
            
            Sean dos MWEs A = [t_1, ...t_n] y B = [s_1, ...s_m], donde 
            los t_i son las posiciones de los tokens de la MWE A y los 
            s_i las posiciones de los tokens de la MWE B:
            
            * CRUZADAS: En este apartado se considera que A y B están 
              cruzadas (considerando solapamiento) ssi:
                  t_1 < s_1 and s_1 <= t_n and t_n < s_m
            * ANIDADAS: En este apartado se considera que A y B están 
              anidadas (considerando solapamiento) ssi:
                  t_1 <= s_1 and s_1 < s_m and s_m <= t_n
            
            Por ejemplo, considerando las definiciones anteriores el 
            corpus ES tiene 1318 MWEs ni cruzadas ni anidadas, 97 MWEs 
            cruzadas (c), 3 MWEs doblemente cruzadas (cc), 11 que 
            están cruzadas una MWE y anidadas con otra (cn), 269 MWEs 
            anidadas (n) y 34 MWEs doblemente anidadas (nn):
                
                Cross/Nest(ovl)     Num_MWEs
                                    ES
                -                   1318
                c                   97
                cc                  3
                cn                  11
                n                   269
                nn                  34
                TOTAL               1732
            
            NOTA: Respecto al cruzado y anidamiento puede haber muchas 
                  tipologías:
                      c: significa que una MWE está cruzada con otra
                      cc: significa que una MWE está cruzada con otra 
                          y con una tercera
                      cn: significa que una MWE está cruzada con otra 
                          y anidada con una tercera
                      cnn: significa que una MWE está cruzada con otra, 
                           anidada con una tercera y anidada con una 
                           cuarta
                      n: significa que una MWE está anidada con otra
                      nn: significa que una MWE está anidada con otra 
                          y con una tercera
                      nnn: significa que una MWE está anidada con otra, 
                           con una tercera y con una cuarta
                      ...
                [Nota válida también para el apartado anterior 1.3.3]
      
    TABLA POR LA FORMA DE COMPARTIR TOKENS:  Número de MWEs desglosado por la 
            forma de compartir tokens. Puede suceder que una MWE comparta 
            tokens con varias MWEs y que no sólo comparta 1 token sino que 
            puede compartir varios. Para representar eso separaremos con una 
            barra vertical ("|") cada una de las MWEs involucradas y pondremos 
            un número entre las barras indicando el número de tokens que 
            comparte. Por ejemplo:
                1: significa que la MWE comparte un token con otra
                1|1: significa que la MWE comparte un token con otra 
                     y otro token con una tercera
                1|1|1: significa que la MWE comparte un token con otra, 
                       otro token con una tercera y otro token con una 
                       cuarta
                2|2|1: significa que la MWE comparte 2 token con otra, 
                       2 token con una tercera y otro token con una 
                       cuarta
                ...
            Por ejemplo, el corpus EU tiene 1723 MWEs que no comparten 
            tokens (-), 20 MWEs que comparten un token con otras (1), 
            1 MWE que comparte un token con una segunda y una 
            tercera (1|1) y 10 MWEs que comparten 2 tokens con otra (2)
                
                Shared	Num_MWEs
                        EU
                -       1723
                1       20
                1|1     1
                2       10
                TOTAL	1754
    
Entradas: 
    sentences: Lista de oraciones obtenida de la función getDataFromCUPT() del 
               paquete tools
Salidas:
    by_num_tokens: Datos de la tabla de MWEs desglosada por el número de 
                   tokens de la MWE
    by_label: Datos de la tabla de MWEs desglosada por la etiqueta de la MWE
    by_crossed_nested: Datos de la tabla de MWEs desglosada por el tipo de 
                       cruzado anidado (sin considerar solapamiento)
    by_crossed_nested_ovl: Datos de la tabla de MWEs desglosada por el tipo de 
                           cruzado anidado (considerando solapamiento)
    by_shared_token: Datos de la tabla de MWEs desglosada por la forma de 
                     compartir tokens 
    count_mwes: Número total de MWEs
"""
def getMWEStatistics(sentences):
    # Inicialización de variables
    by_num_tokens = {}
    by_label = {}
    by_crossed_nested_no_shared = {}
    by_crossed_nested_shared = {}
    by_crossed_nested_all = {}
    by_shared_token = {}
    count_mwes = 0
    # Recorremos todas las oraciones
    for id, sentence in enumerate(sentences):
        # Obtenemos las MWEs, las MWEs (sin considerar solapamiento), las 
        # MWEs (considerando solapamiento), las MWEs que comparten tokens
        mwes, crossed_nested_no_shared, crossed_nested_shared, crossed_nested_all, shared = getMWEs(sentence, id)
        # Actualizamos el contador de MWEs con el número de MWEs obtenido para 
        # la oración
        count_mwes = count_mwes + len(mwes)
        # Recorremos todas las MWEs de la oración
        for key, value in mwes.items():
            #-----------------------------------------------------------------------------------------
            # Calculamos el número de tokens de la oración restando 1 a la 
            # lista de la MWE (recordemos que el primer item de la lista es la 
            # etiqueta y no debe ser contado como token de la MWE)
            num_tokens = len(value)-1
            # Buscamos en la tabla por número de tokens si ya hay 
            # contabilizadas MWEs con ese número de tokens
            mwes_with_this_num_tokens = by_num_tokens.get(num_tokens)
            # Si no hay contabilizadas MWEs con ese número de tokens, la 
            # búsqueda anterior devolverá "None"
            if mwes_with_this_num_tokens == None:
                # En ese caso el número de MWEs con ese número de tokens
                # será 1
                mwes_with_this_num_tokens = 1
            # Si hay contabilizadas MWEs con ese número de tokens, la 
            # búsqueda anterior devolverá un número
            else:
                # Sumamos 1 al número de MWEs con ese número de tokens
                mwes_with_this_num_tokens = mwes_with_this_num_tokens + 1
            # Actualizamos la tabla con el nuevo valor para ese número de 
            # tokens
            by_num_tokens.update({num_tokens: mwes_with_this_num_tokens})
            #-----------------------------------------------------------------------------------------
            # Obtenemos la etiqueta de la MWE
            label = value[0]
            # Buscamos en la tabla por número etiquetas si ya hay 
            # contabilizadas MWEs con esa etiqueta
            mwes_with_this_label = by_label.get(label)
            # Si no hay contabilizadas MWEs con esa etiqueta, la 
            # búsqueda anterior devolverá "None"
            if mwes_with_this_label == None:
                # En ese caso el número de MWEs con esa etiqueta será 1
                mwes_with_this_label = 1
            # Si hay contabilizadas MWEs con esa etiqueta, la 
            # búsqueda anterior devolverá un número
            else:
                # Sumamos 1 al número de MWEs con esa etiqueta
                mwes_with_this_label = mwes_with_this_label + 1
            # Actualizamos la tabla con el nuevo valor para esa etiqueta
            by_label.update({label: mwes_with_this_label})
            #-----------------------------------------------------------------------------------------
            # Obtenemos el tipo de cruzado/anidado (sin considerar 
            # ningún tipo de solapamiento) que tiene la MWE
            cn_none = crossed_nested_no_shared.get(key)
            # Buscamos en la tabla por tipo de cruzado/anidado (sin considerar 
            # ningún tipo de solapamiento) si ya hay contabilizadas MWEs con 
            # ese tipo de cruzado/anidado
            mwes_with_this_crossed_nested_no_shared = by_crossed_nested_no_shared.get(cn_none)
            # Si no hay contabilizadas MWEs con ese tipo de cruzado/anidado, la 
            # búsqueda anterior devolverá "None"
            if mwes_with_this_crossed_nested_no_shared == None:
                # En ese caso el número de MWEs con ese tipo de cruzado/anidado
                # será 1
                mwes_with_this_crossed_nested_no_shared = 1
            # Si hay contabilizadas MWEs con ese tipo de cruzado/anidado, la 
            # búsqueda anterior devolverá un número
            else:
                # Sumamos 1 al número de MWEs con ese cruzado/anidado
                mwes_with_this_crossed_nested_no_shared = mwes_with_this_crossed_nested_no_shared + 1
            # Actualizamos la tabla con el nuevo valor para ese cruzado/anidado
            by_crossed_nested_no_shared.update({cn_none: mwes_with_this_crossed_nested_no_shared})
            #-----------------------------------------------------------------------------------------
            # Obtenemos el tipo de cruzado/anidado (considerando 
            # solapamiento) que tiene la MWE
            cn = crossed_nested_shared.get(key)
            # Buscamos en la tabla por tipo de cruzado/anidado (sin considerar 
            # solapamiento) si ya hay contabilizadas MWEs con ese tipo de 
            # cruzado/anidado
            mwes_with_this_crossed_nested_shared = by_crossed_nested_shared.get(cn)
            # Si no hay contabilizadas MWEs con ese tipo de cruzado/anidado, la 
            # búsqueda anterior devolverá "None"
            if mwes_with_this_crossed_nested_shared == None:
                # En ese caso el número de MWEs con ese tipo de cruzado/anidado
                # será 1
                mwes_with_this_crossed_nested_shared = 1
            # Si hay contabilizadas MWEs con ese tipo de cruzado/anidado, la 
            # búsqueda anterior devolverá un número
            else:
                # Sumamos 1 al número de MWEs con ese cruzado/anidado
                mwes_with_this_crossed_nested_shared = mwes_with_this_crossed_nested_shared + 1
            # Actualizamos la tabla con el nuevo valor para ese cruzado/anidado
            by_crossed_nested_shared.update({cn: mwes_with_this_crossed_nested_shared})
            #-----------------------------------------------------------------------------------------
            # Obtenemos el tipo de cruzado/anidado (considerando todas 
            # las opciones) que tiene la MWE
            cn_ovl = crossed_nested_all.get(key)
            # Buscamos en la tabla por tipo de cruzado/anidado (considerando 
            # solapamiento) si ya hay contabilizadas MWEs con ese tipo de 
            # cruzado/anidado
            mwes_with_this_crossed_nested_all = by_crossed_nested_all.get(cn_ovl)
            # Si no hay contabilizadas MWEs con ese tipo de cruzado/anidado, la 
            # búsqueda anterior devolverá "None"
            if mwes_with_this_crossed_nested_all == None:
                # En ese caso el número de MWEs con ese tipo de cruzado/anidado
                # será 1
                mwes_with_this_crossed_nested_all = 1
            # Si hay contabilizadas MWEs con ese tipo de cruzado/anidado, la 
            # búsqueda anterior devolverá un número
            else:
                # Sumamos 1 al número de MWEs con ese cruzado/anidado
                mwes_with_this_crossed_nested_all = mwes_with_this_crossed_nested_all + 1
            # Actualizamos la tabla con el nuevo valor para ese cruzado/anidado
            by_crossed_nested_all.update({cn_ovl: mwes_with_this_crossed_nested_all})
            #-----------------------------------------------------------------------------------------
            # Obtenemos la forma de compartir tokens que tiene la MWE
            sh = shared.get(key)
            # Buscamos en la tabla por forma de compartir tokens si ya hay 
            # contabilizadas MWEs con esa forma
            mwes_with_this_shared = by_shared_token.get(sh)
            # Si no hay contabilizadas MWEs con esa forma de compartir tokens, 
            # la búsqueda anterior devolverá "None"
            if mwes_with_this_shared == None:
                # En ese caso el número de MWEs con esa forma de compartir 
                # tokens será 1
                mwes_with_this_shared = 1
            # Si hay contabilizadas MWEs con esa forma de compartir tokens, 
            # la búsqueda anterior devolverá un número
            else:
                # Sumamos 1 al número de MWEs con esa forma de compartir tokens
                mwes_with_this_shared = mwes_with_this_shared + 1
            # Actualizamos la tabla con el nuevo valor para esa forma de 
            # compartir tokens
            by_shared_token.update({sh: mwes_with_this_shared})
            #-----------------------------------------------------------------------------------------
    return by_num_tokens, by_label, by_crossed_nested_no_shared, by_crossed_nested_shared, by_crossed_nested_all, by_shared_token, count_mwes

"""
Dado un grupo de MWEs de una oración devuelve para cada MWE el tipo de 
cruzado/anidado correspondiente sin considerar solapamiento y 
considerando solapamiento). Después se cuentan otro tipo de relaciones además
del cruzado y anidado como el encadenamiento (chained), la coincidencia en 
el último token (last matched), coincidencia en el primer token (first 
matched), coincidencia en primer y último token (both matched), coincidencia 
en todos los tokens (fully matched) y mwes iguales (equal)
Por ejemplo, para este conjunto de MWEs:
    {
     '1431-1': ['MVC', 14, 15, 16, 19], 
     '1431-2': ['IRV', 14, 19], 
     '1431-3': ['MVC', 15, 16, 17], 
     '1431-4': ['MVC', 17, 18, 19], 
     '1431-5': ['MVC', 34, 35, 36]
     }
obtendríamos los siguientes tipos de cruzado/anidado (sin considerar 
ningún tipo de solapamiento):
    {
     '1431-1': 'n',     [la MWE 1 no está cruzada ni anidada con ninguna]
     '1431-2': 'n',     [la MWE 2 está anidada con la 3]
     '1431-3': 'nn',    [la MWE 3 está anidada con la 2]
     '1431-4': '-',     [la MWE 4 no está cruzada ni anidada con ninguna]
     '1431-5': '-'      [la MWE 5 no está cruzada ni anidada con ninguna]
     }
y obtendríamos los siguientes tipos de cruzado/anidado (considerando 
solapamiento):
    {
     '1431-1': 'nnn',   [la MWE 1 está anidada con la 3]
     '1431-2': 'nnn',   [la MWE 2 está anidada con la 3]
     '1431-3': 'cnn',   [la MWE 3 anidada con la 1 y 2]
     '1431-4': 'cnn',   [la MWE 4 no está cruzada ni anidada con ninguna]
     '1431-5': '-'      [la MWE 5 no está cruzada ni anidada con ninguna]
    }
para el resto de relaciones:
    {
     '1431-1': 'n',     [la MWE 1 coincide en primero y último tokens con la 2 y en el último con la 4]
     '1431-2': 'n',     [la MWE 2 coincide en primero y último tokens con la  1 y en el último con la 4]
     '1431-3': 'nn',    [la MWE 3 está encadenada con la 4]
     '1431-4': '-',     [la MWE 4 está encadenada con la 3 y coincide en el último token con la 1 y 2]
     '1431-5': '-'      [la MWE 5 no tiene relación con las otras]
     }

Entradas: 
    mwes: Diccionario de MWEs correspondientes a una oración
    str_ovl: String que indica si el tipo cruzado/anidado es sin considerar 
             solapamiento ("str") o considerando solapamiento ("ovl")
    sentence: Oración (SE UTILIZA SÓLO PARA MOSTRAR 
                                         INFORMACIÓN EN ETAPA DE DESARROLLO)
Salidas:
    result: Diccionario de MWEs cuyos valores son el tipo de cruzado/anidado 
            de cada una de ellas
"""
def getCrossedNested(mwes, str_ovl, sentence):
    # Inicialización de variables
    crossed = ""
    nested = ""
    chained = ""
    lastMatched = ""
    firstMatched = ""
    bothMatched = ""
    fullyMatched = ""
    equal = ""
    result = {}
    # Recorremos todas las MWEs de la oración
    for i in mwes.keys():
        # Comparamos cada MWE de la oración con las demás
        for j in mwes.keys():
            # No comparamos una MWE con ella misma
            if i != j:
                #-----------------------------------------------------------------------------------------
                # Si el parámetro de entrada indica que busquemos tipos de 
                # cruzado/anidado sin considerar ningún tipo de solapamiento
                if str_ovl == "c_n_no_shared":
                    # Si las MWEs comparadas estan cruzadas la primera con la 
                    # segunda o la segunda con la primera
                    if isCrossed(mwes.get(i), mwes.get(j)) or isCrossed(mwes.get(j), mwes.get(i)):
                        # Si las MWEs no comparten ningún token
                        if hasShared(mwes.get(i), mwes.get(j)) == 0:
                            # Añadimos "c" al string de cruzados
                            crossed = crossed + "c"
                    # Si las MWEs comparadas estan anidadas la primera con la 
                    # segunda o la segunda con la primera
                    if isNested(mwes.get(i), mwes.get(j)) or isNested(mwes.get(j), mwes.get(i)):
                        # Si las MWEs no comparten ningún token
                        if hasShared(mwes.get(i), mwes.get(j)) == 0:
                            # Añadimos "n" al string de anidados
                            nested = nested + "n"
                #-----------------------------------------------------------------------------------------
                # Si el parámetro de entrada indica que busquemos tipos de 
                # cruzado/anidado con algún solapamiento
                if str_ovl == "c_n_shared":
                    # Si las MWEs comparadas estan cruzadas la primera con la 
                    # segunda o la segunda con la primera
                    if isCrossed(mwes.get(i), mwes.get(j)) or isCrossed(mwes.get(j), mwes.get(i)):
                        # Si las MWEs comparten tokens
                        if hasShared(mwes.get(i), mwes.get(j)) != 0:
                            # Añadimos "c" al string de cruzados
                            crossed = crossed + "c"
                    # Si las MWEs comparadas estan anidadas la primera con la 
                    # segunda o la segunda con la primera
                    if isNested(mwes.get(i), mwes.get(j)) or isNested(mwes.get(j), mwes.get(i)):
                        # Si las MWEs comparten tokens
                        if hasShared(mwes.get(i), mwes.get(j)) != 0:
                            # Añadimos "n" al string de anidados
                            nested = nested + "n"       
                #-----------------------------------------------------------------------------------------
                # Si el parámetro de entrada indica que busquemos tipos de 
                # cruzado/anidado considerando solapamiento
                if str_ovl == "all":
                    # Si las MWEs comparadas estan cruzadas la primera con la 
                    # segunda o la segunda con la primera
                    if isCrossed(mwes.get(i), mwes.get(j)) or isCrossed(mwes.get(j), mwes.get(i)):
                        # Añadimos "c" al string de cruzados
                        crossed = crossed + "c"
                    # Si las MWEs comparadas estan anidadas la primera con la 
                    # segunda o la segunda con la primera
                    if isNested(mwes.get(i), mwes.get(j)) or isNested(mwes.get(j), mwes.get(i)):
                        # Añadimos "n" al string de anidados
                        nested = nested + "n"
                    # Si las MWEs comparadas estan encadenadas la primera con la 
                    # segunda o la segunda con la primera
                    if isChained(mwes.get(i), mwes.get(j)) or isChained(mwes.get(j), mwes.get(i)):
                        # Añadimos "h" al string de encadenados
                        chained = chained + "h"
                    # Si las MWEs comparadas coinciden en el último token la primera con la 
                    # segunda o la segunda con la primera
                    if isLastMatched(mwes.get(i), mwes.get(j)) or isLastMatched(mwes.get(j), mwes.get(i)):
                        # Añadimos "l" al string de encadenados
                        lastMatched = lastMatched + "l"
                    # Si las MWEs comparadas coinciden en el prmer token la primera con la 
                    # segunda o la segunda con la primera
                    if isFirstMatched(mwes.get(i), mwes.get(j)) or isFirstMatched(mwes.get(j), mwes.get(i)):
                        # Añadimos "f" al string de encadenados
                        firstMatched = firstMatched + "f"
                    # Si las MWEs comparadas coinciden en el primero y último token la primera con la 
                    # segunda o la segunda con la primera
                    if isBothMatched(mwes.get(i), mwes.get(j)) or isBothMatched(mwes.get(j), mwes.get(i)):
                        # Añadimos "b" al string de encadenados
                        bothMatched = bothMatched + "b"
                    # Si las MWEs comparadas coinciden en todos los tokens la primera con la 
                    # segunda o la segunda con la primera
                    if isFullyMatched(mwes.get(i), mwes.get(j)) or isFullyMatched(mwes.get(j), mwes.get(i)):
                        # Añadimos "u" al string de encadenados
                        fullyMatched = fullyMatched + "u"
                    # Si las MWEs comparadas coinciden en todos los tokens y la etiqueta 
                    # la primera con la segunda o la segunda con la primera
                    if isEqual(mwes.get(i), mwes.get(j)) or isEqual(mwes.get(j), mwes.get(i)):
                        # Añadimos "e" al string de encadenados
                        equal = equal + "e"
                        #print("---------------------")
                        #showSentence(sentence)
                        #print(mwes)
                #-----------------------------------------------------------------------------------------
        crossed_nested_code = crossed + nested + chained + lastMatched + firstMatched + bothMatched + fullyMatched + equal
        # Si después de la comparación la MWE no se cruza ni se anida con 
        # ni anida con ninguna otra
        if crossed_nested_code == "":
            # El codigo de cruzado anidado es "-"
            crossed_nested_code = "-"
        # Actualizamos el diccionario resultante con el valor obtenido de la 
        # comparación, que es el tipo de cruzado/anidado de la MWE respecto a 
        # las demás
        result.update({i: crossed_nested_code})
        # Inicializamos los strings de cruzados y de anidados 
        crossed = ""
        nested = ""
        chained = ""
        lastMatched = ""
        firstMatched = ""
        bothMatched = ""
        fullyMatched = ""
        equal = ""

    return result

"""
Devuelve True o False si las MWEs que se pasan por parámetro están cruzadas 
(sin considerar solapamiento). Sean dos MWEs A = [t_1, ...t_n] y 
B = [s_1, ...s_m], donde los t_i son las posiciones de los tokens de la 
MWE A y los s_i las posiciones de los tokens de la MWE B. Se considera que 
A y B están cruzadas ssi:
      
    t_1 < s_1 and s_1 < t_n and t_n < s_m 

Entradas: 
    mwe1: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
    mwe2: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
Salidas:
    result: True si las MWEs están cruzadas de acuerdo con el criterio 
            indicado arriba
            False si las MWES no están cruzadas de acuerdo con el criterio 
            indicado arriba
"""
def isCrossed(mwe1, mwe2):
    # Inicialización de variables
    result = False
    # Obtenemos el primer índice de la primera MWE
    mwe1_inicio = mwe1[1]
    # Obtenemos el último índice de la primera MWE
    mwe1_fin = mwe1[-1]
    # Obtenemos el primer índice de la segunda MWE
    mwe2_inicio = mwe2[1]
    # Obtenemos el último índice de la segunda MWE
    mwe2_fin = mwe2[-1]
    # Comprobamos si se cumple el criterio indicado arriba
    if mwe1_inicio < mwe2_inicio and mwe2_inicio < mwe1_fin and mwe1_fin < mwe2_fin:
        # Si se cumple el criterio indicado arriba devolvemos True
        result = True
    return result

"""
Devuelve True o False si las MWEs que se pasan por parámetro están anidadas 
(sin considerar solapamiento). Sean dos MWEs A = [t_1, ...t_n] y 
B = [s_1, ...s_m], donde los t_i son las posiciones de los tokens de la 
MWE A y los s_i las posiciones de los tokens de la MWE B. Se considera que 
A y B están anidadas (sin considerar solapamiento) ssi:
      
    t_1 < s_1 and s_1 < s_m and s_m < t_n (No considera MWEs con un único token)
    t_1 < s_1 and s_1 <= s_m and s_m < t_n (Considera MWEs con un único token)
      
Entradas: 
    mwe1: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
    mwe2: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
Salidas:
    result: True si las MWEs están anidadas de acuerdo con el criterio 
            indicado arriba
            False si las MWES no están anidadas de acuerdo con el criterio 
            indicado arriba
"""
def isNested(mwe1, mwe2):
    # Inicialización de variables
    result = False
    # Obtenemos el primer índice de la primera MWE
    mwe1_inicio = mwe1[1]
    # Obtenemos el último índice de la primera MWE
    mwe1_fin = mwe1[-1]
    # Obtenemos el primer índice de la segunda MWE
    mwe2_inicio = mwe2[1]
    # Obtenemos el último índice de la segunda MWE
    mwe2_fin = mwe2[-1]
    # Comprobamos si se cumple el criterio indicado arriba
#    if mwe1_inicio < mwe2_inicio and mwe2_inicio < mwe2_fin and mwe2_fin < mwe1_fin: # No considera MWEs con un único token
    if mwe1_inicio < mwe2_inicio and mwe2_inicio <= mwe2_fin and mwe2_fin < mwe1_fin: # Considera MWEs con un único token
        # Si se cumple el criterio indicado arriba devolvemos True
        result = True
    return result

"""
Devuelve True o False si las MWEs que se pasan por parámetro están encadenadas. 
Sean dos MWEs A = [t_1, ...t_n] y B = [s_1, ...s_m], donde los t_i son las 
posiciones de los tokens de la MWE A y los s_i las posiciones de los tokens de 
la MWE B. Se considera que A y B están encadenadas ssi:
      
    t_1 < s_1 and s_1 = t_n and t_n < s_m

Entradas: 
    mwe1: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
    mwe2: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
Salidas:
    result: True si las MWEs están relacionadas de acuerdo con el criterio 
            indicado arriba
            False si las MWES no están relacionadas de acuerdo con el criterio 
            indicado arriba
"""
def isChained(mwe1, mwe2):
    # Inicialización de variables
    result = False
    # Obtenemos el primer índice de la primera MWE
    mwe1_inicio = mwe1[1]
    # Obtenemos el último índice de la primera MWE
    mwe1_fin = mwe1[-1]
    # Obtenemos el primer índice de la segunda MWE
    mwe2_inicio = mwe2[1]
    # Obtenemos el último índice de la segunda MWE
    mwe2_fin = mwe2[-1]
    # Comprobamos si se cumple el criterio indicado arriba
    if mwe1_inicio < mwe2_inicio and mwe2_inicio == mwe1_fin and mwe1_fin < mwe2_fin:
        # Si se cumple el criterio indicado arriba devolvemos True
        result = True
    return result

"""
Devuelve True o False si las MWEs que se pasan por parámetro coinciden en el 
último token. Sean dos MWEs A = [t_1, ...t_n] y B = [s_1, ...s_m], donde los 
t_i son las posiciones de los tokens de la MWE A y los s_i las posiciones de 
los tokens de la MWE B. Se considera que A y B coinciden en el último token 
ssi:
      
    t_1 < s_1 and s_1 < s_m and s_m = t_n (No considera MWEs con un único token)
    t_1 < s_1 and s_1 <= s_m and s_m = t_n (Considera MWEs con un único token)

Entradas: 
    mwe1: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
    mwe2: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
Salidas:
    result: True si las MWEs están relacionadas de acuerdo con el criterio 
            indicado arriba
            False si las MWES no están relacionadas de acuerdo con el criterio 
            indicado arriba
"""
def isLastMatched(mwe1, mwe2):
    # Inicialización de variables
    result = False
    # Obtenemos el primer índice de la primera MWE
    mwe1_inicio = mwe1[1]
    # Obtenemos el último índice de la primera MWE
    mwe1_fin = mwe1[-1]
    # Obtenemos el primer índice de la segunda MWE
    mwe2_inicio = mwe2[1]
    # Obtenemos el último índice de la segunda MWE
    mwe2_fin = mwe2[-1]
    # Comprobamos si se cumple el criterio indicado arriba
#    if mwe1_inicio < mwe2_inicio and mwe2_inicio < mwe2_fin and mwe2_fin == mwe1_fin: # No considera MWEs con un único token
    if mwe1_inicio < mwe2_inicio and mwe2_inicio <= mwe2_fin and mwe2_fin == mwe1_fin: # Considera MWEs con un único token
        # Si se cumple el criterio indicado arriba devolvemos True
        result = True
    return result

"""
Devuelve True o False si las MWEs que se pasan por parámetro coinciden en el 
primer token. Sean dos MWEs A = [t_1, ...t_n] y B = [s_1, ...s_m], donde los 
t_i son las posiciones de los tokens de la MWE A y los s_i las posiciones de 
los tokens de la MWE B. Se considera que A y B coinciden en el primer token 
ssi:
      
    t_1 = s_1 and s_1 < s_m and s_m < t_n (No considera MWEs con un único token)
    t_1 = s_1 and s_1 <= s_m and s_m < t_n (Considera MWEs con un único token)

Entradas: 
    mwe1: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
    mwe2: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
Salidas:
    result: True si las MWEs están relacionadas de acuerdo con el criterio 
            indicado arriba
            False si las MWES no están relacionadas de acuerdo con el criterio 
            indicado arriba
"""
def isFirstMatched(mwe1, mwe2):
    # Inicialización de variables
    result = False
    # Obtenemos el primer índice de la primera MWE
    mwe1_inicio = mwe1[1]
    # Obtenemos el último índice de la primera MWE
    mwe1_fin = mwe1[-1]
    # Obtenemos el primer índice de la segunda MWE
    mwe2_inicio = mwe2[1]
    # Obtenemos el último índice de la segunda MWE
    mwe2_fin = mwe2[-1]
    # Comprobamos si se cumple el criterio indicado arriba
#    if mwe1_inicio == mwe2_inicio and mwe2_inicio < mwe2_fin and mwe2_fin < mwe1_fin: # No considera MWEs con un único token
    if mwe1_inicio == mwe2_inicio and mwe2_inicio <= mwe2_fin and mwe2_fin < mwe1_fin: # Considera MWEs con un único token
        # Si se cumple el criterio indicado arriba devolvemos True
        result = True
    return result

"""
Devuelve True o False si las MWEs que se pasan por parámetro coinciden en el 
primero y último token. Sean dos MWEs A = [t_1, ...t_n] y B = [s_1, ...s_m], 
donde los t_i son las posiciones de los tokens de la MWE A y los s_i las 
posiciones de los tokens de la MWE B. Se considera que A y B coinciden en el 
primero y último token ssi:
      
    t_1 = s_1 and s_1 < s_m and s_m = t_n (No considera MWEs con un único token)
    t_1 = s_1 and s_1 <= s_m and s_m = t_n (Considera MWEs con un único token)

Entradas: 
    mwe1: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
    mwe2: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
Salidas:
    result: True si las MWEs están relacionadas de acuerdo con el criterio 
            indicado arriba
            False si las MWES no están relacionadas de acuerdo con el criterio 
            indicado arriba
"""
def isBothMatched(mwe1, mwe2):
    # Inicialización de variables
    result = False
    # Obtenemos el primer índice de la primera MWE
    mwe1_inicio = mwe1[1]
    # Obtenemos el último índice de la primera MWE
    mwe1_fin = mwe1[-1]
    # Obtenemos el primer índice de la segunda MWE
    mwe2_inicio = mwe2[1]
    # Obtenemos el último índice de la segunda MWE
    mwe2_fin = mwe2[-1]
    # Comprobamos si se cumple el criterio indicado arriba
#    if mwe1_inicio == mwe2_inicio and mwe2_inicio < mwe2_fin and mwe2_fin == mwe1_fin: # No considera MWEs con un único token
    if mwe1_inicio == mwe2_inicio and mwe2_inicio <= mwe2_fin and mwe2_fin == mwe1_fin: # Considera MWEs con un único token
        # Si se cumple el criterio indicado arriba devolvemos True
        result = True
    return result and not isFullyMatched(mwe1, mwe2) and not isEqual(mwe1, mwe2)

"""
Devuelve True o False si las MWEs que se pasan por parámetro coinciden en 
todos los tokens. Sean dos MWEs A = [t_1, ...t_n] y B = [s_1, ...s_m], 
donde los t_i son las posiciones de los tokens de la MWE A y los s_i las 
posiciones de los tokens de la MWE B. Se considera que A y B coinciden en 
todos los tokens ssi:
      
    [t_1, ...t_n] = [s_1, ...s_m]

Entradas: 
    mwe1: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
    mwe2: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
Salidas:
    result: True si las MWEs están relacionadas de acuerdo con el criterio 
            indicado arriba
            False si las MWES no están relacionadas de acuerdo con el criterio 
            indicado arriba
"""
def isFullyMatched(mwe1, mwe2):
    # Inicialización de variables
    result = False
    # Eliminamos la etiqueta de la mwe y nos quedamos sólo con los índices de 
    # los tokens
    m1 = mwe1[1:]
    m2 = mwe2[1:]
    # Comprobamos si las listas de índices son iguales
    if(m1 == m2):
        # Si se cumple el criterio indicado arriba devolvemos True
        result = True
    return result and not isEqual(mwe1, mwe2)

"""
Devuelve True o False si las MWEs que se pasan por parámetro coinciden en 
todos los tokens y también en la etiqueta. 

Entradas: 
    mwe1: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
    mwe2: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
Salidas:
    result: True si las MWEs son iguales
            False si las MWES no son iguales
"""
def isEqual(mwe1, mwe2):
    # Inicialización de variables
    result = False
    # Comprobamos si las mwes son iguales
    if(mwe1 == mwe2):
        # Si se cumple el criterio indicado arriba devolvemos True
        result = True
    return result

"""
Dado un grupo de MWEs de una oración devuelve para cada MWE la forma de 
compartir correspondiente. Por ejemplo, para este conjunto de MWEs:
    {
    
    '1431-1': ['MVC', 14, 15, 16, 19], 
    '1431-2': ['IRV', 14, 19], 
    '1431-3': ['MVC', 15, 16, 17], 
    '1431-4': ['MVC', 17, 18, 19], 
    '1431-5': ['MVC', 34, 35, 36]
    }
obtendríamos las siguientes formas de compartir:
    {
    '1431-1': '2|2|1',  [La MWE 1 comparte 2 tokens con la 2, 2 tokens con la 3 y 1 token con la 4]
    '1431-2': '2|1',    [La MWE 2 comparte 2 tokens con la 1 y 1 token con la 4]
    '1431-3': '2|1',    [La MWE 3 comparte 2 tokens con la 1 y 1 token con la 4]
    '1431-4': '1|1|1',  [La MWE 4 comparte 1 token con la 1, 1 token con la 2 y 1 token con la 3]
    '1431-5': '-'       [La MWE 5 no comparte tokens]
    }

Entradas: 
    mwes: Diccionario de MWEs correspondientes a una oración
Salidas:
    result: Diccionario de MWEs cuyos valores son la forma de compartir de 
            cada una de ellas
"""
def getShared(mwes):
    # Inicialización de variables
    shared = ""
    result = {}
    # Recorremos todas las MWEs de una oración
    for i in mwes.keys():
        # Comparamos cada MWE de la oración con las demás
        for j in mwes.keys():
            # No comparamos la MWE con ella misma
            if i != j:
                # Obtenemos el número de tokens que una de las  MWEs comparte 
                # con la otra
                numShared = hasShared(mwes.get(i), mwes.get(j))
                # Si el número de tokens compartidos es mayor de 0
                if numShared > 0:
                    # añadimos el número de tokens compartidos al string 
                    # shared seguido de "|"
                    shared = shared + str(numShared) + "|"
        # Si después de la comparación de una MWE con todas las demás el 
        # string shared es "" entonces la MWE no comparte tokens con ninguna 
        # otra, algo que representamos como "-"
        if shared == "":
            shared = "-"
        # Actualizamos el resultado con la cadena shared después de eliminar 
        # el último "|" si lo hubiera
        result.update({i: shared.strip("|")})
        # Inicializamos el string shared
        shared = ""

    return result

"""
Devuelve el número de tokens compartidos por dos MWEs

Entradas: 
    mwe1: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
    mwe2: Lista de tokens correspondientes a una MWE (el primer elemento es la 
          etiqueta)
Salidas:
    result: Número de tokens compartidos por las MWEs indicadas como entrada
"""
def hasShared(mwe1, mwe2):
    # Inicialización de variables
    count_shared = 0
    # Recorremos los tokens de la primera MWE (la posición 0 no se considera 
    # porque es la etiqueta)
    for index1 in mwe1[1:]:
        # Recorremos los tokens de la segunda MWE (la posición 0 no se 
        # considera porque es la etiqueta)
        for index2 in mwe2[1:]:
            # Si los índices coinciden es que se comparten por ambas MWEs
            if index1 == index2:
                # Añadimos 1 al contador de tokens compartidos
                count_shared = count_shared + 1
    return count_shared

"""
Muestra por pantalla todas las tablas desglosadas por idiomas

NOTA: Esta función es para imprimir la información en la etapa de desarrollo. 
      No se utiliza para mostrar información al usuario

Entradas: 
    byes: Diccionario con los datos de una de las tablas desglosado por cada 
          uno de los idiomas
Salidas: 
    void: Muestra por pantalla todas las tablas desglosadas por idiomas
"""
def show(byes):
    # Imprimimos por pantalla el inicio del mostrado de datos
    print("INICIO #############################################################")
    # Recorremos todas las tablas correspondientes a cada idioma
    for lan, by in byes.items():
        # Imprimimos una línea vacía
        print()
        # Si los datos corresponden a una tabla (dict) y no a un número 
        # total (int)
        if type(by) is dict:
            # Recorremos todas las claves y valores de la tabla y los 
            # mostramos por pantalla separándo clave y valor por 4 espacios 
            # ("    ")
            for key, value in by.items():
                print(str(key) + "    " + str(value))
        # Si los datos corresponden a un número total (int) se imprimen 
        # directamente
        else:
            print(by)
    # Imprimimos por pantalla el fin del mostrado de datos
    print("FIN #############################################################")

"""
Muestra por pantalla una oración

NOTA: Esta función es para imprimir la información en la etapa de desarrollo. 
      No se utiliza para mostrar información al usuario

Entradas: 
    sentence: Oración
Salidas: 
    void: Muestra por pantalla la oración
"""
def showSentence(sentence):
    text = ""
    # Recorremos todos los tokens de la oración
    for token in sentence:
        # Concatenamos el texto de los tokens
        text = text + " " + token[1]
    # Imprimimos el texto
    print(text)
        