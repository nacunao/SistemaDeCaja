class Transaccion:
    
    def __init__(self, numero, asunto, tipo, persona, fecha, ncheque, efectivo, descripcion):
        self.numero = numero
        self.asunto = asunto
        self.tipo = tipo
        self.persona = persona
        self.fecha = fecha
        self.ncheque = ncheque
        self.efectivo = efectivo
        self.descripcion = descripcion