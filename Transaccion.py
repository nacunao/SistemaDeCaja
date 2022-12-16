class Transaccion:
    
    def __init__(self, numero, asunto, tipo, persona, fecha, medioPago, ncheque, monto, descripcion):
        self.numero = numero
        self.asunto = asunto
        self.tipo = tipo
        self.persona = persona
        self.fecha = fecha
        self.medioPago = medioPago
        self.ncheque = ncheque
        self.monto = monto
        self.descripcion = descripcion