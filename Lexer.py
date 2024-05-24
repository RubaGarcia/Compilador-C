from sly import Lexer
import os
import re
import sys

class CLexer(Lexer):
    
    #C tokens
    tokens={
        AUTO, BREAK, CASE, CHAR, CONST, CONTINUE, DEFAULT, DO,                                      # type: ignore
        DOUBLE, ELSE, ENUM, EXTERN, FLOAT, FOR, GOTO, IF, INT,                                      # type: ignore
        LONG, REGISTER, RETURN, SHORT, SIGNED, SIZEOF, STATIC,                                      # type: ignore
        STRUCT, SWITCH, TYPEDEF, UNION, UNSIGNED, VOID, VOLATILE, WHILE                             # type: ignore
        , FLOAT_CONST,  INT_CONST, CHAR_CONST, OBJECTID, PRINT, STRING                              # type: ignore
        , EQ, LE, GE, NE, AND, OR                                                                   # type: ignore 
        # , INCLUDE, LIBRARY                          
        }
        
    literals = {"=","+","-","*","/","(",")","<",">",".",":","@",'"','{','}','~',',',';','[',']','&','!','%','^','|','?'}

    CARACTERES_CONTROL = [bytes.fromhex(i+hex(j)[-1]).decode('ascii')
              for i in ['0', '1']
              for j in range(16)] + [bytes.fromhex(hex(127)[-2:]).decode("ascii")]
    
    #ObjectId hace lo mismo que en el manual de C es el identifier


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

    PRINT = r'\b[pP][rR][iI][nN][tT][fF]\b'
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

    OBJECTID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    #OPERADORES
    EQ = r'=='
    LE = r'<='
    GE = r'>='
    NE = r'!='
    AND = r'&&'
    OR = r'\|\|'


    
    # INCLUDE = r'\#include'

    # LIBRARY = r'\b\<.+\.h\>\b'

    @_(r'\t| |\v|\r|\f')
    def spaces(self, t):
        pass

    @_(r'\b[0-9]+\.[0-9]+\b')
    def FLOAT_CONST(self, t):
        return t
    
    @_(r'\b[0-9]*\.[0-9]+\b')
    def FLOAT_CONST(self, t):
        return t
    
    @_(r'\b[0-9]+\.[0-9]*\b')
    def FLOAT_CONST(self, t):
        return t

    INT_CONST = r'\b[0-9]+\b'

    CHAR_CONST = r"\'[a-zA-Z0-9]\'"

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    # @_(r';')
    # def EOI(self, t):
    #     self.lineno += t.value.count(';') 

    @_(r'\/\/.*')
    def line_comment(self, t):
        self.lineno += t.value.count('\n')
        pass
    
    #multiline comment
    @_(r'\/\*')
    def multiline_comment(self, t):
        self.begin(MultilineCommentRemover)
        pass

    @_(r'\"(.*?)\"')
    def STRING(self, t):
        return t

    #keywords c99

    #keywords GNU

    #CONSTANTES

    # INT_CONST = r'\b[0-9]+\b'

    # FLOAT_CONST = r'\b[0-9]+\.[0-9]+\b'

    # CHAR_CONST = r'\b\'[a-zA-Z0-9]\'\b'



class MultilineCommentRemover(Lexer):

    tokens = {}
    _nestcomments = 0

    @_(r'\/\*')
    def anidar(self, t):
        self._nestcomments += 1
        pass
    
    @_(r'\/\*')
    def ignorar_apertura(self, t):
        if (t.value[1] == '\n'):
            self.lineno += 1
        pass

    @_(r'\*\/')
    def desanidar(self, t):
        if self._nestcomments == 0:
            self.begin(CLexer)
        else:
            self._nestcomments -= 1
        pass

    @_(r'\n')
    def newline(self, t):
        self.lineno += 1

    @_(r'.')
    def CUALQUIERCOSA(self, t):
        pass

    @_(r'\/\*')
    def anidar(self, t):
        self._nestcomments += 1
        pass

    @_(r'\*\/')
    def desanidar(self, t):
        if self._nestcomments == 0:
            self.begin(CLexer)
        else:
            self._nestcomments -= 1
        pass

    @_(r'\n')
    def newline(self, t):
        self.lineno += 1

    @_(r'.')
    def CUALQUIERCOSA(self, t):
        pass

if __name__ == '__main__':
    text = '''
    int constantes(){
        int i = 0;
        if (i == 1){
            printf("Hola")
        }else{
            printf("Adios")
        }
    }
'''
    '''
    //#include <stdio.h>
    //definición de primeras variables


    int prev1 = 1;
    int prev2 = 0;

    /*
    función de fibonacci
    f(n)=f(n-1)+f(n-2)
    */
    void fib(int n) {
        if (n < 3) {
            return;
        }
        int fn = prev1 + prev2;
        prev2 = prev1;
        prev1 = fn;
        printf("%d ", fn);
        return fib(n - 1);
    }

    void printFib(int n) {
        if (n < 1) {
            printf("Invalid number of terms\n");
        } else if (n == 1) {
            printf("%d ", 0);
        } else if (n == 2) {
            printf("%d %d", 0, 1);
        } else {
            printf("%d %d ", 0, 1);
            fib(n);
        }
    }

    int main() {
        int n = 9; // Change this value to print a different number of terms
        printFib(n);
        return 0;
    }
    '''
    lexer = CLexer()
    for tok in lexer.tokenize(text):
        print(tok)