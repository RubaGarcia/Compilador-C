from sly import Lexer
import os
import re
import sys

class CLexer(Lexer):
    
    #C tokens
        tokens={OBJECTID, 
            AUTO, BREAK, CASE, CHAR, CONST, CONTINUE, DEFAULT, DO,
            DOUBLE, ELSE, ENUM, EXTERN, FLOAT, FOR, GOTO, IF, INT,
            LONG, REGISTER, RETURN, SHORT, SIGNED, SIZEOF, STATIC,
            STRUCT, SWITCH, TYPEDEF, UNION, UNSIGNED, VOID, VOLATILE, WHILE
            INT_CONST, FLOAT_CONST, CHAR_CONST, STRING_CONST}
        
        literals = {':', ';', ',', '(', ')', '{', '}', '+', '-', '*', '/', '<', '=', '>', '@', '~', '.'}

        CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
                  for i in ['0', '1']
                  for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]
    
    #ObjectId hace lo mismo que en el manual de C es el identifier

    OBJECTID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    #Palabras reservadas de C
    AUTO = r'\b[aA][uU][tT][oO]\b'

    CASE = r'\b[cC][aA][sS][eE]\b'

    CHAR = r'\b[cC][hH][aA][rR]\b'

    CONST = r'\b[cC][oO][nN][sS][tT]\b'

    CONTINUE = r'\b[cC][oO][nN][tT][iI][nN][uU][eE]\b'

    DEFAULT = r'\b[dD][eE][fF][aA][uU][lL][tT]\b'

    DO = r'\b[dD][oO]\b'

    DOUBLE = r'\b[dD][oO][uU][bB][lL][eE]\b'

    ELSE =  r'\b[eE][lL][sS][eE]\b'

    ENUM = r'\b[eE][nN][uU][mM]\b'

    EXTERN = r'\b[eE][xX][tT][eE][rR][nN]\b'

    FLOAT = r'\b[fF][lL][oO][aA][tT]\b'

    FOR = r'\b[fF][oO][rR]\b'

    GOTO = r'\b[gG][oO][tT][oO]\b'

    IF = r'\b[iI][fF]\b'

    INT = r'\b[iI][nN][tT]\b'

    LONG = r'\b[lL][oO][nN][gG]\b'

    REGISTER = r'\b[rR][eE][gG][iI][sS][tT][eE][rR]\b'

    RETURN = r'\b[rR][eE][tT][uU][rR][nN]\b'

    SHORT = r'\b[sS][hH][oO][rR][tT]\b'

    SIGNED = r'\b[sS][iI][gG][nN][eE][dD]\b'

    SIZEOF = r'\b[sS][iI][zZ][eE][oO][fF]\b'

    STATIC = r'\b[sS][tT][aA][tT][iI][cC]\b'

    STRUCT = r'\b[sS][tT][rR][uU][cC][tT]\b'

    SWITCH = r'\b[sS][wW][iI][tT][cC][hH]\b'

    TYPEDEF = r'\b[tT][yY][pP][eE][dD][eE][fF]\b'

    UNION = r'\b[uU][nN][iI][oO][nN]\b'

    UNSIGNED = r'\b[uU][nN][sS][iI][gG][nN][eE][dD]\b'

    VOID = r'\b[vV][oO][iI][dD]\b'

    VOLATILE = r'\b[vV][oO][lL][aA][tT][iI][lL][eE]\b'

    WHILE = r'\b[wW][hH][iI][lL][eE]\b'

    #keywords c99

    #keywords GNU

    #CONSTANTES

    # INT_CONST = r'\b[0-9]+\b'

    # FLOAT_CONST = r'\b[0-9]+\.[0-9]+\b'

    # CHAR_CONST = r'\b\'[a-zA-Z0-9]\'\b'

