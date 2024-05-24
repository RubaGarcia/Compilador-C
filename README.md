# Compilador-C
Repo de desarrollo de un compilador de ANSI C para la asignatura de Lenguajes de Programación
**FORMA DE EJECUTAR EL COMPILADOR ES EJECUTANDO EL MAIN**
Información obtenida del [manual de C](https://www.gnu.org/software/gnu-c-manual/gnu-c-manual.html) 
## Indice
1. [Lexer](#Lexer)
2. [Parser](#Parser)
3. [Traducción a Python](#Traducción-a-Python)

## Lexer
En el lexer hemos tomado todas las keywords de C y las hemos añadido a la lista de tokens, además de añadir los tokens de los operadores y los delimitadores. Como hemos hecho durante el desarrollo de las prácticas en grupo, tambien hemos implementado un lexer auxiliar para ignorar los comentarios.

## Parser
En el parser hemos tenido que rehacer las estructuras que toma el parser para que se ajusten a las necesidades de C. 

Como se observa hay tokens no utilizados, ésto es porque por falta de tiempo no ha sido posible implementar todas las funcionalidades de C.

Entre las Funcionalidades nuevas que hemos añadido respecto al compilador de cool tenemos:
- Return
- Break
- Ciertas operaciones lógicas(Or, And, GtIgual...)

## Traducción a Python
Hemos rehecho bastantes clases, algunas se quedan sin tocar porque en C son innecesarias(clases, llamadas a métodos estaticos...) tambien una de las grandes diferencias es que en C no hay ámbitos debidos a las clases, por lo que nos libramos de mucha carga de trabajo.


