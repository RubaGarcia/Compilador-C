import os
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
