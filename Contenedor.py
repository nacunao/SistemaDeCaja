class Contenedor:

    def __init__(self):
        # Diccionario que contiene las trasacciones
        self.diccionario_transacciones={}
        self.lista_recibido_de=[]
        self.lista_enviado_a=[]

    # Función buscarTransaccion
    def buscarTransaccion(self, id):
        if id in self.diccionario_transacciones:
            return True
        else: return False
    
    # Función agregarTransaccion
    def agregarTransaccion(self, nuevaTransaccion, id):
        if self.buscarTransaccion(id) == True:
            return
        else:
            self.diccionario_transacciones[id] = nuevaTransaccion