'''import os
import re
import sys
import io

dir = os.path.expanduser("./")
sys.path.append(dir)

from Lexer import CLexer

debug = True
num_lines = 3
sys.path.append(dir)
dir = os.path.join(dir, "Lexer-01", "Tests")
ficheros = os.listdir(dir)
tests = [fich for fich in ficheros
         if os.path.isfile(os.path.join(dir, fich)) and
         re.search(r"^[a-zA-Z].*\.(c)$", fich)]

tests.sort()
print(tests)

contador = len(tests)
for fich in tests:
    lexer = CLexer()
    f = open(os.path.join(dir, fich), 'r', newline='')
    g = open(os.path.join(dir, fich + '.out'), 'r', newline='')
    if os.path.isfile(os.path.join(dir, fich)+'.nuestro'):
        os.remove(os.path.join(dir, fich)+'.nuestro')
    if os.path.isfile(os.path.join(dir, fich)+'.bien'):
        os.remove(os.path.join(dir, fich)+'.bien')
    texto = ''
    entrada = f.read()
    f.close()
    texto = '\n'.join(lexer.salida(entrada))
    texto = f'#name "{fich}"\n' + texto
    resultado = g.read()
    texto = re.sub(r'#\d+\b', '', texto)
    resultado = re.sub(r'#\d+\b', '', resultado)
    texto = re.sub(r'\s+\n', '\n', texto)
    resultado = re.sub(r'\s+\n', '\n', resultado)
    g.close()
    if texto.strip().split() != resultado.strip().split():
        print(f"Revisa el fichero {fich}")
        if debug:
            nuestro = [linea for linea in texto.split('\n') if linea]
            bien = [linea for linea in resultado.split('\n') if linea]
            linea = 0
            f = open(os.path.join(dir, fich)+'.nuestro', 'w')
            g = open(os.path.join(dir, fich)+'.bien', 'w')
            f.write(texto.strip())
            g.write(resultado.strip())
            f.close()
            g.close()
            contador -= 1'''