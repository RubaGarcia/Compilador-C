# coding: utf-8

from Lexer import CLexer
from sly import Parser
import sys
import os
from Clases import *



class CParser(Parser):
    nombre_fichero = ""
    tokens = CLexer.tokens
    debugfile = 'parser.out'
    errores = []
    # precedence = (
    #     ('left', 'ASSIGN'),
    #     ('left', 'IN'),
    #     ('nonassoc', 'LE', '<', '='), # Nonassociative operators
    #     ('left', '+', '-'),
    #     ('left', '*', '/'),
    #     ('right', 'NOT', 'ISVOID', '~'),
    #     ('left', '@'),
    #     ('left', '.')
    # )

    @_("listlineas")
    def Programa(self, p):
        return Programa(cuerpo=p[0])

    @_("Programa listlineas")
    def Programa(self, p):
        return Programa(secuencia=p[0].secuencia + [p[1]])

    # @_("Clase")
    # def Programa(self, p):
    #     return Programa(secuencia=[p[0]])

    @_("")
    def optAssign(self, p):
        return None

    

    @_("'=' Expression")
    def optAssign(self, p):
        return p[1]
    
    #PRINTS
    @_("PRINT '(' STRING ')' ';' ")
    def Expression(self, p):
        return Print(cuerpo=p[1])
    
    @_("PRINT '(' STRING argumentos ')' ';' ")
    def Expression(self, p):
        return Print(cuerpo=p[1], argumentos=p[2])

    @_("',' Expression")
    def argumentos(self, p):
        return [p[1]]   
    
    @_("',' Expression argumentos")
    def argumentos(self, p):
        return [p[1]] + p[2]
    #RETURN
    @_("RETURN Expression ")
    def Expression(self, p):
        return Return(cuerpo=p[1])

    @_("RETURN ")
    def Expression(self, p):
        return Return(cuerpo="None")

    #tipos
    @_("INT")
    def tipo(self, p):
        return p[0]

    @_("FLOAT")
    def tipo(self, p):
        return p[0]
    
    @_("CHAR")
    def tipo(self, p):
        return p[0]
    
    @_("VOID")
    def tipo(self, p):
        return p[0]
    
    #operaciones binarias

    @_("Expression '+' Expression")
    def Expression(self, p):
        return Suma(p[0], p[2])
    
    @_("Expression '-' Expression")
    def Expression(self, p):
        return Resta(p[0], p[2])
    
    @_("Expression '*' Expression")
    def Expression(self, p):
        return Multiplicacion(p[0], p[2])
    
    @_("Expression '/' Expression")
    def Expression(self, p):
        return Division(p[0], p[2])
    
    #CONSTS

    @_("INT_CONST")
    def Expression(self, p):
        return Entero(p[0])
    
    @_("FLOAT_CONST")
    def Expression(self, p):
        return Flotante(valor = p[0])
    
    @_("CHAR_CONST")
    def Expression(self, p):
        return String(valor = p[0])
    
    @_("OBJECTID")
    def Expression(self, p):
        return Objeto(nombre=p[0])

    # @_('"=" Expression')
    # def optAssign(self, p):
    #     return p[1]

    # @_("INT OBJECTID optAssign ';'")
    # def Atributo(self, p):
    #     return Atributo(tipo=p[0], nombre=p[1], valor=p[2])
    
    # @_("FLOAT OBJECTID optAssign ';'")
    # def Atributo(self, p):
    #     return Atributo(tipo=p[0], nombre=p[1], valor=p[2])
    
    # @_("CHAR OBJECTID optAssign ';'")
    # def Atributo(self, p):
    #     return Atributo(tipo=p[0], nombre=p[1], valor=p[2])
    
    @_("tipo OBJECTID optAssign ';' ")
    def Atributo(self, p):
        return Atributo(tipo=p[0], nombre=p[1], cuerpo=p[2])

    #Metodo y formal

    @_("tipo OBJECTID '(' ')' '{' bloque '}' ';'")
    def Metodo(self, p):
        return Metodo(tipo=p[0], nombre=p[1], formales=p[3], cuerpo=p[5])
    
    @_("tipo OBJECTID '(' listaFormales ')' '{' bloque '}' ';'")
    def Metodo(self, p):
        return Metodo(tipo=p[0], nombre=p[1], formales=p[3], cuerpo=p[6])
    
    @_("Formal")
    def listaFormales(self, p):
        return [p[0]]
    
    @_("tipo OBJECTID")
    def Formal(self, p):
        return Formal(tipo=p[0], nombre_variable=p[1])

    @_("Expression ';'")
    def bloque(self, p):
        return [p[0]]
    
    @_("Expression ';' bloque")
    def bloque(self, p):
        return [p[0]] + p[2]
    
    @_("'(' Expression ')'")
    def Expression(self, p):
        return p[1]

    #operaciones logicas
    @_("Expression '<' Expression")
    def Expression(self, p):
        return Menor(izquierda=p[0], derecha=p[2])
    
    @_("Expression '<' '=' Expression")
    def Expression(self, p):
        return LeIgual(izquierda=p[0], derecha=p[2])
    
    @_("Expression '>' '=' Expression")
    def Expression(self, p):
        return GtIgual(izquierda=p[0], derecha=p[2])
    
    @_("Expression '=' '=' Expression")
    def Expression(self, p):
        return Igual(izquierda=p[0], derecha=p[2])
    
    @_("Expression '!' '=' Expression")
    def Expression(self, p):
        return Not(expr = Igual(izquierda=p[0], derecha=p[2]))
    
    @_("'!' Expression")
    def Expression(self, p):
        return Not(expr = p[1])
    
    @_("Expression '&' '&' Expression ")
    def Expression(self, p):
        return And(izquierda=p[0], derecha=p[3])
    
    @_("Expression '|' '|' Expression ")
    def Expression(self, p):
        return Or(izquierda=p[0], derecha=p[3])
    
    #if

    @_("IF '(' Expression ')' '{' bloque '}'")
    def Expression(self, p):
        return Condicional(condicion=p[2], verdadero=p[5], falso="continue")

    @_("IF '(' Expression ')' '{' bloque '}' Continuacion")
    def Expression(self, p):
        return Condicional(condicion=p[2], verdadero=p[5], falso=p[7])
    
    @_("ELSE '{' bloque '}'")
    def Continuacion(self, p):
        return p[2]

    @_("ELSE IF '(' Expression ')' '{' bloque '}' Continuacion")
    def Continuacion(self, p):
        return Condicional(condicion=p[3], verdadero=p[6], falso=p[0])

    @_("ELSE IF '(' Expression ')' '{' bloque '}'")
    def Continuacion(self, p):
        return Condicional(condicion=p[3], verdadero=p[6], falso="continue")

    #While
    @_("WHILE '(' Expression ')' '{' bloque '}'")
    def Expression(self, p):
        return Bucle(condicion=p[2], bloque=p[5])

    #
    @_("Atributo")
    def Linea(self, p):
        return p[0]
    
    @_("Metodo")
    def Linea(self, p):
        return p[0]
    
    @_("Expression")
    def Linea(self, p):
        return p[0]
    
    @_("Linea")
    def listlineas(self, p):
        return [p[0]]
    
    @_("Linea listlineas")
    def listlineas(self, p):
        return [p[0]] + p[1]



    # @_("'{' bloque'}'")
    # def Expression(self, p):
    #     return Bloque(expresiones=p[1])

    # @_("Expresion ';'")
    # def bloque(self, p):
    #     return p[0]

    def error(self,p):
        self.errores.append("Error de sintaxis en la linea " + str(p.lineno) + " en el token " + str(p.value))



    
