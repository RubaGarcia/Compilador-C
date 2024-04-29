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
        , INT_CONST, FLOAT_CONST, CHAR_CONST, STRING_CONST, STRING
        }
        
    literals = {':', ',', '(', ')', '{', '}', '+', '-', '*', '/', '<', '=', '>', '@', '~', '.', #';'
                }

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
    
    @_(r'\t| |\v|\r|\f')
    def spaces(self, t):
        pass

    INT_CONST = r'[0-9]+'

    FLOAT_CONST = r'\b[0-9]+\.[0-9]+\b'

    #STRING_CONST = r'\"[a-zA-Z0-9]*\"'
    @_(r'\"')
    def STRING_CONST(self, t):
        self.begin(StringLexer)
        pass

    CHAR_CONST = r'\b\'[a-zA-Z0-9]\'\b'

    STRING = r'[Ss][Tt][Rr][Ii][Nn][Gg]'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r';')
    def EOI(self, t):
        self.lineno += t.value.count(';') 

    @_(r'\/\/')
    def line_comment(self, t):
        self.lineno += t.value.count('\n')
        pass
    
    #multiline comment
    @_(r'\/\*')
    def multiline_comment(self, t):
        self.begin(MultilineCommentRemover)
        pass
    #keywords c99

    #keywords GNU

    #CONSTANTES

    # INT_CONST = r'\b[0-9]+\b'

    # FLOAT_CONST = r'\b[0-9]+\.[0-9]+\b'

    # CHAR_CONST = r'\b\'[a-zA-Z0-9]\'\b'

class StringLexer(Lexer):
    tokens ={STRING_CONST, RETORNO, ESCAPADO, X}

    _recursion = ""

    #escapoados
    @_(r'\\\n')
    def ESCNL(self,t):
        self._recursion = "\\n"
        pass

    @_(r'\\\"')
    def ESCQ(self,t):
        self._recursion = "\\\""
        pass

    @_(r'\t')
    def TAB(self,t):
        self._recursion = "\t"
        pass
    
    #TODO revisar en el manual
    @_(r'\\[^btnrf\\]')
    def ESCAPADO(self,t):
        self._recursion = t.value[1:]
        pass

    @_(r'\\[btnrf\\]')
    def ESCAPADO2(self,t):
        self._recursion = t.value
        pass

    @_(r'\"')
    def RETORNO(self,t):
        t.type = "STRING_CONST"
        t.value = str(self._recursion)
        self._recursion = ""
        self.begin(CLexer)
        t.value = "\""+t.value+"\""
        return t
    
    @_(r'(.\Z)|(.\x00)') #error de string
    def ERROR(self,t):
        t.value = "error en fichero"
        self.begin(CLexer)
        return t
    
    @_(r'\n') #error \ en salto de linea
    def ERROR2(self,t):
        t.type = "ERROR"
        t.value = '"Unterminated string constant"'
        self._recursion = ""
        self.begin(CLexer)
        return t
    
    @_(r'.')
    def X(self,t):
        self._recursion += t.value
        pass

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
    int main(){
        int previo1 = 1;
        int previo2 = 1;
        for(int i = 0; i < 10;i++){
            int fn = previo1 + previo2;
            previo2 = previo1;
            previo1 = fn;
            printf("%d ", fn);
        }
    }
    '''
    lexer = CLexer()
    for tok in lexer.tokenize(text):
        print(tok)