# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 01:04:36 2025

Clase ejecutable para la realización de conteos y estadísticas sobre los 
ficheros cupt del corpus.


Entradas:
    <corpus_folder>: Directorio donde están las carpetas que contienen cada 
                     idioma
    <language> el idioma sobre el que se va a realizar el conteo (hará 
               referencia al subdirectorio de la carpeta 'corpus' donde se 
               encuentren los cupt del idioma correspondiente, es decir, ES, 
               EU, ...). Si se indica "ALL" o no se especifica un idioma, 
               se realizará el conteo sobre todos los idiomas que contenga la 
               carperta del corpus
Salidas:
    Imprime por pantalla todos los conteos relativos al idioma pasado por 
    parámetro o bien las de todos los idiomas si en el parámetro 
    <language> se ha especificado "ALL"

@author: sflanza
"""

import sys
import os
import counter

def main():
    # Si el usuario no ha introducido todos los parámetros
    if len(sys.argv) < 2:
        print("Usage: python do_count.py <corpus_folder> <language> [language --> ALL or unspecified for all languages]")
        return
    # Añade "/" al final del parámetro 1 si no la tiene
    if not sys.argv[1].endswith("/"):
        sys.argv[1] = sys.argv[1] + "/"
    # Si el segundo parámetro no se ha especificado se añade la cadena 
    # vacía ("") a la lista de parámetros
    if len(sys.argv) == 2:
        sys.argv.append("")
    # Si el parámetro 1 es el directorio del corpus
    if os.path.isdir(sys.argv[1]):
        # Imprimimos los conteos correspondeintes al idioma especificado o a 
        # todos según lo que se indque en el parámetro segundo
        counter.print_data(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
