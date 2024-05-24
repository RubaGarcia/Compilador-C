# coding: utf-8

from Lexer import CLexer
from sly import Parser
import sys
import os
from Clases import *

class CParser(Parser):
    tokens = CLexer.tokens
    debugfile = 'parser.out'
    errores = []
    precedence = (
        ('nonassoc', '<', '='), # Nonassociative operators
        ('left', '+', '-'),
        ('left', '*', '/')
    )
    

    # @_("INCLUDE LIBRARY")
    # def include(self,p):
    #     return Include(p.LIBRARY)

    @_("listLineas")
    def Programa(self,p):
        return Programa(secuencia=p[0])
    
    
    @_("Linea listLineas")
    def listLineas(self,p):
        return [p[0]] + p[1]

    @_("Linea")
    def listLineas(self,p):
        return [p[0]]
    
    @_("Bucle")
    def Linea(self,p):
        return p[0]
    
    @_("WHILE '(' Expression ')' '{' listLineas '}'")
    def Bucle(self,p):
        return Bucle(condicion=p[2],cuerpo=Bloque(expresiones=p[5]))
    
    # @_("Condicional")
    # def Linea(self,p):
    #     return p[0]
    
    @_("IF '(' Expression ')' '{' listLineas '}' Continuacion")
    def Expression(self,p):
        return Condicional(condicion=p[2],verdadero=p[5],falso=p[7])
    
    @_("IF '(' Expression ')' '{' listLineas '}'")
    def Expression(self,p):
        return Condicional(condicion=p[2],verdadero=p[5],falso="continue")
    
    @_("ELSE IF '(' Expression ')' '{' listLineas '}'")
    def Continuacion(self,p):
        return Condicional(condicion=p[3],verdadero=p[6],falso="continue")
    
    @_("ELSE IF '(' Expression ')' '{' listLineas '}' Continuacion")
    def Continuacion(self,p):
        return Condicional(condicion=p[3],verdadero=p[6],falso=p[8])
    
    @_("ELSE '{' listLineas '}'")
    def Continuacion(self,p):
        return p[2]

    @_("Metodo")
    def Linea(self,p):
        return p[0]
    
    @_("tipo OBJECTID '(' ')' '{' listLineas '}'")
    def Metodo(self,p):
        return Metodo(tipo=p[0],nombre=p[1],cuerpo=Bloque(expresiones=p[5]))
    
    @_("tipo OBJECTID '(' listaFormales ')' '{' listLineas '}'")
    def Metodo(self,p):
        return Metodo(tipo=p[0],nombre=p[1],formales=p[3],cuerpo=Bloque(expresiones=p[6]))
    
    @_("INT")
    def tipo(self,p):
        return p[0]
    
    @_("CHAR")
    def tipo(self,p):
        return p[0]
    
    @_("FLOAT")
    def tipo(self,p):
        return p[0]
    
    @_("DOUBLE")
    def tipo(self,p):
        return p[0]
    
    @_("VOID")
    def tipo(self,p):
        return p[0]
    
    @_("Formal")
    def listaFormales(self, p):
        return [p[0]]

    @_("Formal ',' listaFormales")
    def listaFormales(self, p):
        return [p[0]] + p[2]
    
    @_("tipo OBJECTID")
    def Formal(self,p):
        return Formal(tipo=p[0],nombre_variable=p[1])


    # --RETORNO--
    @_("Retorno")
    def Linea(self,p):
        return p[0]
    
    @_("RETURN Expression ';'")
    def Retorno(self,p):
        return Return(cuerpo=p[1])
    
    @_("RETURN ';'")
    def Retorno(self,p):
        return Return(cuerpo=None)
    

    # --IMPRIMIR--
    @_("Imprimir")
    def Linea(self,p):
        return p[0]

    @_("PRINT '(' STRING ')' ';'")
    def Imprimir(self,p):
        return Print(texto=p[2])
    
    @_("PRINT '(' STRING argumentos ')' ';'")
    def Imprimir(self,p):
        return Print(texto=p[2],argumentos=p[3])
    
    @_("',' Expression")
    def argumentos(self,p):
        return [p[1]]
    
    @_("',' Expression argumentos")
    def argumentos(self,p):
        return [p[1]] + p[2]


    
    @_("Expression ';'")
    def Linea(self,p):
        return p[0]
    
    @_("tipo OBJECTID optAssign")
    def Expression(self,p):
        return Atributo(tipo=p[0],nombre=p[1],cuerpo=p[2])

    @_("")
    def optAssign(self,p):
        return NoExpr()
    
    @_("'=' Expression")
    def optAssign(self,p):
        return p[1]



    # @_("tipo OBJECTID optAssign ';'")
    # def Atributo(self,p):
    #     return Atributo(tipo=p[0],nombre=p[1],valor=p[2])
    
    # @_("tipo OBJECTID optAssign ';'")
    # def Atributo(self,p):
    #     return Atributo(tipo=p[0],nombre=p[1],valor=p[2])
    
    # @_("DOUBLE OBJECTID optAssign ';'")
    # def Atributo(self,p):
    #     return Atributo(tipo=p[0],nombre=p[1],valor=p[2])
    
    
    # @_("LONG OBJECTID optAssign ';'")
    # def Atributo(self,p):
    #     return Atributo(tipo=p[0],nombre=p[1],valor=p[2])
    
    # @_("SHORT OBJECTID optAssign ';'")
    # def Atributo(self,p):
    #     return Atributo(tipo=p[0],nombre=p[1],valor=p[2])
    
    # @_("Atributo")
    # def Expression(self,p):
    #     return p[0]

    @_("OBJECTID '=' Expression ';'")
    def Expression(self,p):
        return Asignacion(nombre=p[0],cuerpo=p[2])

    @_("OBJECTID")    
    def Expression(self,p):
        return Objeto(nombre=p[0])
    
    @_("INT_CONST")
    def Expression(self,p):
        return Entero(valor=p[0])
    
    @_("CHAR_CONST")
    def Expression(self,p):
        return String(valor=p[0])
    
    @_("FLOAT_CONST")
    def Expression(self,p):
        return Flotante(valor=p[0])
    
    @_("Expression '+' Expression")
    def Expression(self,p):
        return Suma(izquierda=p[0],derecha=p[2])
    
    @_("Expression '-' Expression")
    def Expression(self,p):
        return Resta(izquierda=p[0],derecha=p[2])
    
    @_("Expression '*' Expression")
    def Expression(self,p):
        return Multiplicacion(izquierda=p[0],derecha=p[2])
    
    @_("Expression '/' Expression")
    def Expression(self,p):
        return Division(izquierda=p[0],derecha=p[2])
    
    # @_("Atributo")
    # def Expression(self, p):
    #     return p[0]
  
    # @_("Expression ';'")
    # def bloque(self, p):
    #     return [p[0]]
    
    # @_("Expression ';' bloque")
    # def bloque(self, p):
    #     return [p[0]] + p[2]
    
    # @_("Expression bloque")
    # def bloque(self, p):
    #     return [p[0]] + p[1]


    
    #break
    @_("BREAK ';'")
    def Expression(self,p):
        return Break()
    
    @_("'(' Expression ')'")
    def Expression(self,p):
        return p[1]
    
    @_("Expression '<' Expression")
    def Expression(self,p):
        return Menor(izquierda=p[0],derecha=p[2])
    
    @_("Expression LE Expression")
    def Expression(self,p):
        return LeIgual(izquierda=p[0],derecha=p[2])
    
    @_("Expression '>' Expression")
    def Expression(self,p):
        return Mayor(izquierda=p[0],derecha=p[2])
    
    @_("Expression GE Expression")
    def Expression(self,p):
        return GtIgual(izquierda=p[0],derecha=p[2])
    
    @_("Expression EQ Expression")
    def Expression(self,p):
        return Igual(izquierda=p[0],derecha=p[2])
    
    @_("Expression NE Expression")
    def Expression(self,p):
        return Not(Expression=Igual(izquierda=p[0],derecha=p[2]))
    
    @_("'!' Expression")
    def Expression(self,p):
        return Not(Expression=p[1])
    
    @_("Expression AND Expression")
    def Expression(self,p):
        return And(izquierda=p[0],derecha=p[2])
    
    @_("Expression OR Expression")
    def Expression(self,p):
        return Or(izquierda=p[0],derecha=p[2])
    
    
    

    @_("OBJECTID '(' ')'")
    def Expression(self,p):
        return LlamadaMetodo(nombre_metodo=p[0])

    @_("OBJECTID '(' listaExpresiones ')'")
    def Expression(self,p):
        return LlamadaMetodo(nombre_metodo=p[0],argumentos=p[2])
    
    @_("Expression")
    def listaExpresiones(self,p):
        return [p[0]]
    
    @_("Expression ',' listaExpresiones")
    def listaExpresiones(self,p):
        return [p[0]] + p[2]
    
    # @_("Bucle")
    # def Linea(self,p):
    #     return p[0]
    
    # @_("Atributo")
    # def Linea(self,p):
    #     return p[0]
    
    # @_("Metodo")
    # def Linea(self,p):
    #     return p[0]
    
    # @_("Condicional")
    # def Linea(self,p):
    #     return p[0]
    
    @_("Expression")
    def Linea(self,p):
        return p[0]
    

    
