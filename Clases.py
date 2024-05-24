# coding: utf-8
from dataclasses import dataclass, field
from typing import List
import re



dict_global = {"padre": None}

numeroIfs = 0
numeroBucle = 0

@dataclass
class Nodo:
    linea: int = 0

    def str(self, n):
        return f'{n*" "}#{self.linea}\n'
    
    #FIXME Nodo
    def genera_codigo(self, n=0):
        return ""
    


@dataclass
class Formal(Nodo):
    nombre_variable: str = '_no_set'
    tipo: str = '_no_type'
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_formal\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        return resultado
    
    def genera_codigo(self, n=0):
        return f'{self.nombre_variable}'



class Expresion(Nodo):
    cast: str = '_no_type'
    
#funcion nueva que implementa el break
@dataclass
class Break(Expresion):
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_break\n'
        return resultado
    
    def genera_codigo(self, n=0):
        return f'{(n)*" "}break\n'

#funcion nueva que implementa el return 
@dataclass
class Return(Expresion):
    cuerpo: str = '_no_set'
    def genera_codigo(self, n=0):

        if self.cuerpo is not "None":
            codigo = f'{(n)*" "}return {self.cuerpo.genera_codigo(0)}\n'
        else:
            codigo = f'{(n)*" "}return None\n'
        return codigo
        # return f'{(n)*" "}return {self.cuerpo.genera_codigo(0)}\n'

#funcion que implementa el print    
@dataclass
class Print(Expresion):
    texto: str = '_no_set'
    argumentos: List[Expresion] = field(default_factory=list)

    def genera_codigo(self, n=0):
        # print(self.texto)
        codigo = ""
        codigo += f'{(n)*" "}print({self.texto}'
        if len(self.argumentos) > 0:
            codigo += f'% ({self.argumentos[0].genera_codigo(0)}'

            for arg in self.argumentos[1:]:
                codigo += f', {arg.genera_codigo(0)}'
            codigo += ')'
        codigo += ', end=\'\')\n'
        return codigo

@dataclass
class Asignacion(Expresion):
    nombre: str = '_no_set'
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_assign\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):
        # print(self.nombre)
        # print(self.cuerpo)
        codigo = ""
        codigo += f'{(n)*" "}{self.nombre} = {self.cuerpo.genera_codigo(0)}\n'
        #FIXME
        return codigo



@dataclass
class LlamadaMetodoEstatico(Expresion):
    cuerpo: Expresion = None
    clase: str = '_no_type'
    nombre_metodo: str = '_no_set'
    argumentos: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_static_dispatch\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n+2)*" "}{self.clase}\n'
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: _no_type\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        variable = self.cuerpo.genera_codigo(0, dict_recibido)
        codigo += f'{" "*n}temp_class = {variable}\n'
        codigo += f'{" "*n}temp_class.__class__ = {self.clase}\n'
        # codigo += f'{" "*n}temp_class.{self.nombre_metodo}('
        # if len(self.argumentos) > 0:
        #     for arg in self.argumentos[:-1]:
        #         codigo += f'{arg.genera_codigo(0, dict_recibido)}, '
        #     codigo += f'{self.argumentos[-1].genera_codigo(0, dict_recibido)}'
        # codigo += f')'
        argumentos = ""
        if len(self.argumentos) > 0:
            for i in range(len(self.argumentos)-1):
                codigo += self.argumentos[i].genera_codigo(n, dict_recibido) + '\n'
                codigo += f'arg{i} = temp\n'
                argumentos += f'arg{i}, '
            codigo += self.argumentos[len(self.argumentos)-1].genera_codigo(n, dict_recibido) + '\n'
            codigo += f'{" "*n}arg{len(self.argumentos)-1} = temp\n'
            argumentos += f'arg{len(self.argumentos)-1}'

        codigo += f'{" "*n}temp_class.{self.nombre_metodo}({argumentos})'


        return codigo
    
    



@dataclass
class LlamadaMetodo(Expresion):
    cuerpo: Expresion = None
    nombre_metodo: str = '_no_set'
    argumentos: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_dispatch\n'
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n+2)*" "}{self.nombre_metodo}\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.argumentos])
        resultado += f'{(n+2)*" "})\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    

    def genera_codigo(self, n=0):
        codigo = ""
        argumentos = ""
        if len(self.argumentos) > 0:
            # for i in range(len(self.argumentos)-1):
            #     codigo += self.argumentos[i].genera_codigo(n, dict_recibido) + '\n'
            #     codigo += f'arg{i} = temp\n'
            #     argumentos += f'arg{i}, '
            # codigo += self.argumentos[len(self.argumentos)-1].genera_codigo(n, dict_recibido) + '\n'
            # codigo += f'{" "*n}arg{len(self.argumentos)-1} = temp\n'
            # argumentos += f'arg{len(self.argumentos)-1}'
            for i in range(len(self.argumentos)-1):
                argumentos += f'{self.argumentos[i].genera_codigo(0)}, '
            argumentos += f'{self.argumentos[-1].genera_codigo(0)}'

        codigo += f'{(n)*" "}{self.nombre_metodo}({argumentos})'

        return codigo


@dataclass
class Condicional(Expresion):
    condicion: Expresion = None
    verdadero: Expresion = None
    falso: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_cond\n'
        resultado += self.condicion.str(n+2)
        resultado += self.verdadero.str(n+2)
        resultado += self.falso.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):
        # print(self.condicion)
        # print(self.verdadero)
        # print(self.falso)
        codigo=""
        # codigo += self.condicion.genera_codigo(n)
        # codigo += '\n'
        global numeroIfs
        numeroIfs += 1
        
        codigo += f'{(n)*" "}condicion{numeroIfs} = {self.condicion.genera_codigo(0)}\n'
        codigo += f'{(n)*" "}if (condicion{numeroIfs} == True):\n'
        for linea in self.verdadero:
            codigo += f'{linea.genera_codigo(n+2)}\n'

        # codigo += f'{self.verdadero.genera_codigo(n+2)}\n'
        
        codigo += f'{(n)*" "}else:\n'
        if not isinstance(self.falso, list):
            if self.falso is "continue":
                codigo += f'{(n+2)*" "}pass\n'
            else:
                codigo += f'{self.falso.genera_codigo(n+2)}\n'
        else:
            for linea in self.falso:
                codigo += f'{linea.genera_codigo(n+2)}\n'
        return codigo



@dataclass
class Bucle(Expresion):
    condicion: Expresion = None
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_loop\n'
        resultado += self.condicion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):
        codigo = ""
        # codigo += self.condicion.genera_codigo(n, dict_recibido)
        # codigo += '\n'
        global numeroBucle
        numeroBucle += 1
        codigo += f'{" "*n}condicionW{numeroBucle} = {self.condicion.genera_codigo(0)}\n'
        codigo += f'{(n)*" "}while (condicionW{numeroBucle} == true):\n'
        codigo += f'{self.cuerpo.genera_codigo(n+2)}\n'
        codigo += f'{" "*(n+2)}condicionW{numeroBucle} = {self.condicion.genera_codigo(0)}\n'
        return codigo


@dataclass
class Let(Expresion):
    nombre: str = '_no_set'
    tipo: str = '_no_set'
    inicializacion: Expresion = None
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_let\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.inicializacion.str(n+2)
        resultado += self.cuerpo.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
    #     #similar to lambda expression
        variable = self.nombre
        dict_actual = {"padre": dict_recibido}
        dict_actual.update({self.nombre: None})
        codigo = ""
        # codigo += f'{n*" "}let {variable} : '
        # codigo += f'{self.tipo}'
        # codigo += f'({self.inicializacion.genera_codigo(0, dict_recibido)})'
        # codigo += f' in {self.cuerpo.genera_codigo(0, dict_actual)}\n'

        # codigo += f'{n*" "}temp = lambda {variable} : {self.cuerpo.genera_codigo(0, dict_recibido)}\n'
        # codigo += f'{n*" "}temp({self.tipo}({self.inicializacion.genera_codigo(0, dict_recibido)}))\n'
        codigo += self.inicializacion.genera_codigo(n, dict_actual)
        codigo += '\n'
        codigo += f'{(n)*" "}def temp_func({self.nombre}):\n'
        # codigo += f'{(n+2)*" "}{self.inicializacion.genera_codigo(0)}\n'
        codigo += f'{self.cuerpo.genera_codigo(n+2, dict_actual)}\n'
        codigo += f'{(n)*" "}variable = {self.tipo}(temp)\n'
        codigo += f'{(n)*" "}temp_func(variable)\n'
        return codigo
    
        # codigo = ""
        # codigo += f'{(n)*" "}{self.nombre} = {self.inicializacion.genera_codigo(0)}\n'
        # codigo += f'{self.cuerpo.genera_codigo(n)}'
        # return codigo
    #FIXME Let


@dataclass
class Bloque(Expresion):
    expresiones: List[Expresion] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado = f'{n*" "}_block\n'
        resultado += ''.join([e.str(n+2) for e in self.expresiones])
        resultado += f'{(n)*" "}: {self.cast}\n'
        resultado += '\n'
        return resultado

    def genera_codigo(self, n=0):
        codigo = ""
        
        for expr in self.expresiones:
            codigo += f'{expr.genera_codigo(n)}\n'
        
        return codigo


@dataclass
class RamaCase(Nodo):
    nombre_variable: str = '_no_set'
    cast: str = '_no_set'
    tipo: str = '_no_set'
    cuerpo: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_branch\n'
        resultado += f'{(n+2)*" "}{self.nombre_variable}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado
    #FIXME RamaCase
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        codigo = f'{(n)*" "}case {self.tipo}:\n'
        codigo += f'{self.cuerpo.genera_codigo(n+2, dict_recibido)}'
        # lista_retorno = []
        # contador = 0
        # for elemento in reversed(self.cuerpo.genera_codigo(n, dict_recibido)):
        #         if elemento == '\n':
        #             break
        #         else:
        #             lista_retorno.append(elemento)
        #             contador += 1
        # codigo += f'{self.cuerpo.genera_codigo(n+2, dict_recibido)[0:-contador]}'
        # codigo += f'{(n+2)*" "}return ({"".join(reversed(lista_retorno))})\n'
        return codigo

@dataclass
class Swicht(Expresion):
    expr: Expresion = None
    casos: List[RamaCase] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_typcase\n'
        resultado += self.expr.str(n+2)
        resultado += ''.join([c.str(n+2) for c in self.casos])
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
        
    #FIXME Swicht NO FUNCIONA NADA BIEN

    def genera_codigo(self, n=0, dict_recibido=dict_global):
        
        #usamos un diccionario para hacer el switch
        codigo = ""
        codigo = f'{(n)*" "}match {self.expr.genera_codigo(0, dict_recibido)}:\n'
        for caso in self.casos:
            codigo += f'{caso.genera_codigo(n+2, dict_recibido)}'
            # codigo += f'{caso.cuerpo.genera_codigo(n+4, dict_recibido)}'
        return codigo

        
        # codigo = ""
        # codigo = f'{(n)*" "}switch {self.expr.genera_codigo(0)}:\n'
        # for caso in self.casos:
        #     codigo += caso.genera_codigo(n+2)
            


@dataclass
class Nueva(Expresion):
    tipo: str = '_no_set'
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_new\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def genera_codigo(self, n=0):
        codigo = ""
        # codigo = f'{(n)*" "}new {self.tipo}'
        codigo = f'{(n)*" "}'
        return codigo
        #FIXME Nueva


@dataclass
class OperacionBinaria(Expresion):
    izquierda: Expresion = None
    derecha: Expresion = None



@dataclass
class Suma(OperacionBinaria):
    operando: str = '+'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_plus\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):
        codigo = ""
        # codigo += self.izquierda.genera_codigo(n, dict_recibido)
        # codigo += f'\n'
        # codigo += f'{(n)*" "}temp0 = temp\n'
        # codigo += self.derecha.genera_codigo(n, dict_recibido)
        # codigo += f'\n{(n)*" "}temp = temp + temp0'
        codigo = f'{self.izquierda.genera_codigo(n)} + {self.derecha.genera_codigo(0)}'

         
        #si no existen las variables en el diccionario las creamos y inicializamos a 0?
    #    if(self.izquierda.genera_codigo(0, dict_recibido) not in dict_recibido.keys()):
    #        dict_recibido.update({self.izquierda.genera_codigo(0, dict_recibido): 0})
            
    #    if(self.derecha.genera_codigo(0, dict_recibido) not in dict_recibido.keys()):
    #        dict_recibido.update({self.derecha.genera_codigo(0, dict_recibido): 0})
            

        
        
        return codigo

@dataclass
class Resta(OperacionBinaria):
    operando: str = '-'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_sub\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):

        codigo = ""

        # codigo += self.izquierda.genera_codigo(n, dict_recibido)
        # codigo += f'\n'
        # codigo += f'{(n)*" "}temp0 = temp\n'
        # codigo += self.derecha.genera_codigo(n, dict_recibido)
        # codigo += f'\n{(n)*" "}temp = temp0 - temp'

        codigo = f'{self.izquierda.genera_codigo(n)} - {self.derecha.genera_codigo(0)}'
        return codigo



@dataclass
class Multiplicacion(OperacionBinaria):
    operando: str = '*'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_mul\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):    
        codigo = ""

        # codigo += self.izquierda.genera_codigo(n, dict_recibido)
        # codigo += f'\n'
        # codigo += f'{(n)*" "}temp0 = temp\n'
        # codigo += self.derecha.genera_codigo(n, dict_recibido)
        # codigo += f'\n{(n)*" "}temp = temp0 * temp'

        codigo = f'{self.izquierda.genera_codigo(n)} * {self.derecha.genera_codigo(0)}'
        return codigo

@dataclass
class Division(OperacionBinaria):
    operando: str = '/'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_divide\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):    
        codigo = ""
        
        # codigo += self.izquierda.genera_codigo(n, dict_recibido)
        # codigo += f'\n'
        # codigo += f'{(n)*" "}temp0 = temp\n'
        # codigo += self.derecha.genera_codigo(n, dict_recibido)
        # codigo += f'\n{(n)*" "}temp = temp0 / temp'

        codigo = f'{self.izquierda.genera_codigo(n)} / {self.derecha.genera_codigo(0)}'
        return codigo

@dataclass
class Menor(OperacionBinaria):
    operando: str = '<'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_lt\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):    
        codigo = ""
        # codigo += self.izquierda.genera_codigo(n, dict_recibido)
        # codigo += f'\n'
        # codigo += f'{(n)*" "}temp0 = temp\n'
        # codigo += self.derecha.genera_codigo(n, dict_recibido)
        # codigo += f'\n{(n)*" "}temp = temp0 < temp'

        codigo = f'({self.izquierda.genera_codigo(n)} < {self.derecha.genera_codigo(0)})'
        return codigo

#nueva clase de Meyor
@dataclass
class Mayor(OperacionBinaria):
    operando: str = '>'
    def genera_codigo(self, n=0):
        codigo = f'({self.izquierda.genera_codigo(n)} > {self.derecha.genera_codigo(0)})'
        return codigo


@dataclass
class LeIgual(OperacionBinaria):
    operando: str = '<='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_leq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):    
        codigo = ""

        # codigo += self.izquierda.genera_codigo(n, dict_recibido)
        # codigo += f'\n'
        # codigo += f'{(n)*" "}temp0 = temp\n'
        # codigo += self.derecha.genera_codigo(n, dict_recibido)
        # codigo += f'\n{(n)*" "}temp = temp0 <= temp'


        codigo = f'({self.izquierda.genera_codigo(n)} <= {self.derecha.genera_codigo(0)})'
        return codigo


@dataclass
class Igual(OperacionBinaria):
    operando: str = '='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_eq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):    
        codigo = ""

        # codigo += self.izquierda.genera_codigo(n, dict_recibido)
        # codigo += f'\n'
        # codigo += f'{(n)*" "}temp0 = temp\n'
        # codigo += self.derecha.genera_codigo(n, dict_recibido)
        # codigo += f'\n{(n)*" "}temp = temp == temp0'

        codigo += f'({self.izquierda.genera_codigo(n)} == {self.derecha.genera_codigo(0)})'

        return codigo

@dataclass
class GtIgual(OperacionBinaria):
    operando: str = '>='

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_geq\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):    
        codigo = ""

        # codigo += self.izquierda.genera_codigo(n, dict_recibido)
        # codigo += f'\n'
        # codigo += f'{(n)*" "}temp0 = temp\n'
        # codigo += self.derecha.genera_codigo(n, dict_recibido)
        # codigo += f'\n{(n)*" "}temp = temp0 >= temp'

        codigo = f'({self.izquierda.genera_codigo(n)} >= {self.derecha.genera_codigo(0)})'
        return codigo

##clases nuevas para los operadores de OR y AND

@dataclass
class Or(OperacionBinaria):
    operando: str = 'or'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_or\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):    
        codigo = ""

        codigo += f'({self.izquierda.genera_codigo(n)} or {self.derecha.genera_codigo(0)})'
        
        return codigo
    
@dataclass
class And(OperacionBinaria):
    operando: str = 'and'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_and\n'
        resultado += self.izquierda.str(n+2)
        resultado += self.derecha.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):    
        codigo = ""

        codigo += f'({self.izquierda.genera_codigo(n)} and {self.derecha.genera_codigo(0)})'
        
        return codigo

@dataclass
class Neg(Expresion):
    expr: Expresion = None
    operador: str = '~'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_neg\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):    
        codigo = ""
        codigo = f'(not {self.expr.genera_codigo(0)})'
        return codigo

@dataclass
class Not(Expresion):
    expr: Expresion = None
    operador: str = 'NOT'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_comp\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'not {self.expr.genera_codigo(0)}'
        return codigo

@dataclass
class EsNulo(Expresion):
    expr: Expresion = None

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_isvoid\n'
        resultado += self.expr.str(n+2)
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        codigo = f'{self.expr.genera_codigo(0, dict_recibido)}.isVoid()'
        return codigo

@dataclass
class Objeto(Expresion):
    nombre: str = '_no_set'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_object\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo += f'{(n)*" "}{self.nombre}'
        return codigo
    


@dataclass
class NoExpr(Expresion):
    nombre: str = ''

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_no_expr\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def genera_codigo(self, n=0):
        return "None"


@dataclass
class Entero(Expresion):
    valor: int = 0

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_int\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{(n)*" "}{self.valor}'
        # codigo += "temp = "
        return codigo

#clase nueva para flotante
@dataclass
class Flotante(Expresion):
    valor: float = 0.0

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_float\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{(n)*" "}{self.valor}'
        return codigo

@dataclass
class String(Expresion):
    valor: str = '_no_set'

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_string\n'
        resultado += f'{(n+2)*" "}{self.valor}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado
    
    def genera_codigo(self, n=0):
        codigo = ""
        codigo = f'{(n)*" "}{self.valor}'
        return codigo


@dataclass
class Booleano(Expresion):
    valor: bool = False
    
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_bool\n'
        resultado += f'{(n+2)*" "}{1 if self.valor else 0}\n'
        resultado += f'{(n)*" "}: {self.cast}\n'
        return resultado

    def genera_codigo(self, n=0, dict_recibido=dict_global):
        codigo = ""
        #codigo = f'{(n)*" "}{True if self.valor else False}'
        codigo += f'{" "*n}temp = Bool({self.valor})'
        return codigo
        

@dataclass
class IterableNodo(Nodo):
    secuencia: List = field(default_factory=List)


class Programa(IterableNodo):
    def str(self, n):
        resultado = super().str(n)
        resultado += f'{" "*n}_program\n'
        resultado += ''.join([c.str(n+2) for c in self.secuencia])
        return resultado
    
    def genera_codigo(self, n=0): # genera codigo tiene que tener un indentado 
        #----------------------------------
        

        codigo =""
        for clase in self.secuencia:
            codigo += clase.genera_codigo(n)

        codigo += f"{' '*n}main()\n"

        return codigo
        #----------------------------------

@dataclass
class Caracteristica(Nodo):
    nombre: str = '_no_set'
    tipo: str = '_no_set'
    cuerpo: Expresion = None
    

@dataclass
class Clase(Nodo):
    nombre: str = '_no_set'
    padre: str = '_no_set'
    nombre_fichero: str = '_no_set'
    caracteristicas: List[Caracteristica] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_class\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.padre}\n'
        resultado += f'{(n+2)*" "}"{self.nombre_fichero}"\n'
        resultado += f'{(n+2)*" "}(\n'
        resultado += ''.join([c.str(n+2) for c in self.caracteristicas])
        resultado += '\n'
        resultado += f'{(n+2)*" "})\n'
        return resultado
    
    #------------------
    def genera_codigo(self,n=0, dict_recibido=dict_global):
        codigo =""
        codigo = f"{' '*n}class {self.nombre}({self.padre}):\n"
        global dict_global
            # if (self.caracteristicas is not []):
        # for caracteristica in self.caracteristicas[0]:
        for caracteristica in self.caracteristicas:
            if (isinstance(caracteristica, Atributo)):
                codigo += f"{' '*(n+2)}def __init__(self):\n"
                break
        for caracteristica in self.caracteristicas:
            if (isinstance(caracteristica, Atributo)):
               # lista_atributos.append(caracteristica.nombre)
                dict_global.update({caracteristica.nombre: None}) # FIXME
                codigo += caracteristica.genera_codigo(n+4)
        for caracteristica in self.caracteristicas:
            if (not isinstance(caracteristica, Atributo)):
                codigo += caracteristica.genera_codigo(n+2, dict_global) # FIXME
        return codigo
    #-------------------

@dataclass
class Metodo(Caracteristica):
    formales: List[Formal] = field(default_factory=list)

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_method\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += ''.join([c.str(n+2) for c in self.formales])
        resultado += f'{(n + 2) * " "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)

        return resultado
    
    def genera_codigo(self,n=0):      
        # print(self.formales)
        # print(self.cuerpo)
        # print(self.linea)
        # print(self.nombre)
        
        # global lista_atributos
        # nuevo_ambito = {"padre": dict_recibido}
        # codigo = ""
        codigo = f'{(n)*" "}def {self.nombre}('
        if len(self.formales) > 0:
            codigo += f'{self.formales[0].genera_codigo(0)}'
            for i in range(1,len(self.formales)):
                codigo += f', {self.formales[i].genera_codigo(0)}'

            
        codigo += '):\n'   
        codigo += self.cuerpo.genera_codigo(n+2)
        #codigo += f'{(n+2)*" "}return {self.cuerpo.genera_codigo(0, nuevo_ambito)[-1]}\n'
        
        return codigo


class Atributo(Caracteristica):

    def str(self, n):
        resultado = super().str(n)
        resultado += f'{(n)*" "}_attr\n'
        resultado += f'{(n+2)*" "}{self.nombre}\n'
        resultado += f'{(n+2)*" "}{self.tipo}\n'
        resultado += self.cuerpo.str(n+2)
        return resultado

    def genera_codigo(self,n=0): 

        if self.cuerpo is None:
            codigo = f'{(n)*" "}{self.nombre} = {self.tipo.capitalize()}(None)\n'
        else:
            codigo = f'{(n)*" "}{self.nombre} = {self.cuerpo.genera_codigo(0)}\n'
        
        return codigo
