class Contenedor:

    def __init__(self):
        self.lista_recibido_de=[]
        self.lista_enviado_a=[]

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
