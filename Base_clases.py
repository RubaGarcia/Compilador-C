from copy import deepcopy

class Object:
    # def __init__(self,s) -> None:
    #     pass
    estaInicializado = False
    
    def abort(self):
        # exit()
        print("error")

    def copy(self):
        return deepcopy(self)

    def isVoid(self):
        return not self.estaInicializado


class Int(Object):
    def __init__(self, s):
        super().__init__()
        self.estaInicializado = True
        if s is None:
            self.numero = 0
        else:
            self.numero = s

    def __sub__(self, s):
        if (isinstance(s, Int)):
            return Int(self.numero - s.numero)
            # return Int(0)
        else:
            return Int(self.numero - s)
            
        
    def __add__(self, s):
        if (isinstance(s, Int)):
            return Int(self.numero + s.numero)
        else:
            return Int(self.numero + s)
            
class Flotante(Object):
    def __init__(self, s):
        super().__init__()
        self.estaInicializado = True
        if s is None:
            self.numero = 0.0
        else:
            self.numero = s

    def __sub__(self, s):
        if (isinstance(s, Flotante)):
            return Flotante(self.numero - s.numero)
        else:
            return Flotante(self.numero - s)
            
    def __add__(self, s):
        if (isinstance(s, Flotante)):
            return Flotante(self.numero + s.numero)
        else:
            return Flotante(self.numero + s)
    
class Bool(Object):
    def __init__(self, s):
        super().__init__()
        self.estaInicializado = True
        if s is None:
            self.booleano = False
        else:
            self.booleano = s

    def __eq__(self, e1):
        if (isinstance(e1, Bool)):
            return self.booleano == e1.booleano
        else:
            return self.booleano == e1

true = Bool(True)
false = Bool(False)
