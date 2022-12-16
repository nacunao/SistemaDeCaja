class Contenedor:

    def __init__(self):
        # Diccionario que contiene las trasacciones
        self.diccionario_ingresos={}
        self.diccionario_egresos={}
        self.lista_recibido_de=[]
        self.lista_enviado_a=[]

    
    
    # Función agregarIngreso
    def agregarIngreso(self, nuevaTransaccion, id):
        if self.buscarTransaccion(id) == True:
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