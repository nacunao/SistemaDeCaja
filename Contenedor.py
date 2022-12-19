class Contenedor:

    def __init__(self):
        # Diccionario que contiene las trasacciones
        self.diccionario_ingresos={}
        self.diccionario_egresos={}
        self.lista_recibido_de=[]
        self.lista_enviado_a=[]

    
    
    # Función agregarIngreso
    def agregarIngreso(self, nuevaTransaccion, id):
        if self.buscarIngreso(id) == True:
            return
        else:
            self.diccionario_ingresos[id] = nuevaTransaccion

    # Función buscarIngreso
    def buscarIngreso(self, id):
        if id in self.diccionario_ingresos:
            return True
        else: return False

    # Función agregarEgreso
    def agregarEgreso(self, nuevaTransaccion, id):
        if self.buscarEgreso(id) == True:
            return
        else:
            self.diccionario_egresos[id] = nuevaTransaccion

    # Función buscarEgreso
    def buscarEgreso(self, id):
        if id in self.diccionario_egresos:
            return True
        else: return False

    # Función agregarRecibidoDe
    def agregarRecibidoDe(self, nuevoRecibidoDe):
        if self.buscarRecibidoDe(nuevoRecibidoDe) == True:
            return
        else:
            self.lista_recibido_de.append(nuevoRecibidoDe)

    # Función eliminarRecibidoDe
    def eliminarRecibidoDe(self, nuevoRecibidoDe):
        if self.buscarRecibidoDe(nuevoRecibidoDe) == False:
            return
        else:
            self.lista_recibido_de.remove(nuevoRecibidoDe)

    # Funcion buscarRecibidoDe
    def buscarRecibidoDe(self, nuevoRecibidoDe):
        i=0
        while i<len(self.lista_recibido_de):
            if(self.lista_recibido_de[i]==nuevoRecibidoDe):
                return True
            i=i+1
        return False

    # Función agregarEnviadoA
    def agregarEnviadoA(self, nuevoEnviadoA):
        if self.buscarEnviadoA(nuevoEnviadoA) == True:
            return
        else:
            self.lista_enviado_a.append(nuevoEnviadoA)

    # Función eliminarEnviadoA
    def eliminarEnviadoA(self, nuevoEnviadoA):
        if self.buscarEnviadoA(nuevoEnviadoA) == False:
            return
        else:
            self.lista_enviado_a.remove(nuevoEnviadoA)

    # Funcion buscarEnviadoA
    def buscarEnviadoA(self, nuevoEnviadoA):
        i=0
        while i<len(self.lista_enviado_a):
            if(self.lista_enviado_a[i]==nuevoEnviadoA):
                return True
            i=i+1
        return False
