from Contenedor import *
from Transaccion import *
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkcalendar import Calendar, DateEntry
from datetime import *

# Contenedor: contiene el diccionario de transacciones, la lista de enviado a/recido de
c = Contenedor()

#====================================VENTANA PRINCIPAL=========================================
class Menu(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Menu")
        self.config(width=500, height=500)
        self.master.resizable(width=False, height=False)

        
        self.boton1=Button(self, text="Agregar Ingreso", command=self.abrir_ventanaSecundaria1, font=("Helvetica", 13), activebackground='#78d6ff')
        self.boton1.place(x=150, y=50,  height=50, width=200)

        self.boton2=Button(self, text="Agregar Egreso", command=self.abrir_ventanaSecundaria2, font=("Helvetica", 13), activebackground='#78d6ff')
        self.boton2.place(x=150, y=150,  height=50, width=200)

        self.boton3=Button(self,text="Mostrar Listado", command=self.abrir_ventanaSecundaria3, font=("Helvetica", 13), activebackground='#78d6ff')
        self.boton3.place(x=150, y=250, height=50, width=200)

    def abrir_ventanaSecundaria1(self):
        self.master.withdraw()
        self.nuevaVentana=VentanaSecundariaAgregarIngreso()

    def abrir_ventanaSecundaria2(self):
        self.master.withdraw()
        self.nuevaVentana=VentanaSecundariaAgregarEgreso()

    def abrir_ventanaSecundaria3(self):
        self.master.withdraw()
        self.nuevaVentana=VentanaSecundariaMostrarListado()

#=================================VENTANA SECUNDARIA AGREGAR INGRESO===========================
class VentanaSecundariaAgregarIngreso(Frame):
    def __init__(self):
        nuevo=Frame.__init__(self)
        nuevo=Toplevel(self)
        nuevo.title("Agregar Ingreso")
        nuevo.config(width=750, height=750)
        nuevo.resizable(width=False, height=False)
        
        self.asunto_var=StringVar()
        self.persona_var=StringVar()
        self.medioPago_var=StringVar()
        self.ncheque_var=StringVar()
        self.monto_var=StringVar()
        self.descripcion_var=StringVar()
        self.imprimir=BooleanVar()

        # Titulo
        self.titulo=Label(nuevo, text="Ingreso", font=("Helvetica", 20))
        self.titulo.place(x=40, y=10)

        # Etiquetas
        self.etiqueta1=Label(nuevo, text="Asunto:", font=("Helvetica", 13))
        self.etiqueta1.place(x=40, y=60)

        self.etiqueta2=Label(nuevo, text="Recibido de:", font=("Helvetica", 13))
        self.etiqueta2.place(x=40, y=120)

        self.etiqueta3=Label(nuevo, text="Fecha:", font=("Helvetica", 13))
        self.etiqueta3.place(x=40, y=180)

        self.etiqueta4=Label(nuevo, text="N Cheque:", font=("Helvetica", 13))
        self.etiqueta4.place(x=40, y=300)

        self.etiqueta5=Label(nuevo, text="Monto:", font=("Helvetica", 13))
        self.etiqueta5.place(x=40, y=360)

        self.etiqueta6=Label(nuevo, text="Por concepto de:", font=("Helvetica", 13))
        self.etiqueta6.place(x=40, y=420)

        # Entradas
        self.entrada1=Entry(nuevo, textvariable=self.asunto_var, font=("Helvetica", 13))
        self.entrada1.place(x=200, y=60, width=500, height=32)

        self.entrada2=ttk.Combobox(nuevo, textvariable=self.persona_var, font=("Helvetica", 13))
        self.entrada2['values']=c.lista_recibido_de,"nuevo"
        self.entrada2.place(x=200, y=120, width=500, height=32)

        self.entrada3=DateEntry(nuevo, width=50)
        self.entrada3.place(x=200, y=180, width=200, height=32)
        self.entrada3.config(headersbackground="#E62B0A", headersforeground="#ffffff", foreground="#000000", background="#ffffff")

        self.entrada4=Entry(nuevo, textvariable=self.ncheque_var, font=("Helvetica", 13))
        self.entrada4.place(x=200, y=300, width=500, height=32)

        self.entrada5=Entry(nuevo, textvariable=self.monto_var, font=("Helvetica", 13))
        self.entrada5.place(x=200, y=360, width=500, height=32)

        self.entrada6=scrolledtext.ScrolledText(nuevo, wrap=WORD, font=("Helvetica", 13))
        self.entrada6.place(x=200, y=420, width=500, height=118)

        # Botones radio
        self.radioBoton1=Radiobutton(nuevo, text="Cheque", font=("Helvetica", 13), variable=self.medioPago_var, value="Cheque")
        self.radioBoton1.place(x=200, y=240)
        self.radioBoton1.select()

        self.radioBoton2=Radiobutton(nuevo, text="Efectivo", font=("Helvetica", 13), variable=self.medioPago_var, value="Efectivo")
        self.radioBoton2.place(x=300, y=240)
        
        self.radioBoton3=Radiobutton(nuevo, text="Transferencia", font=("Helvetica", 13), variable=self.medioPago_var, value="Transferencia")
        self.radioBoton3.place(x=400, y=240)

        # CheckBox
        self.checkBox=Checkbutton(nuevo, text="¿Desea imprimir los datos del ingreso en pdf?", variable=self.imprimir, onvalue=1, offvalue=0, font=("Helvetica", 12))
        self.checkBox.place(x=40, y=560)  

        # Botones
        self.boton_volver=Button(nuevo, text="Regresar", command=self.cerrar_ventanaSecundaria, font=("Helvetica", 13), activebackground='#78d6ff')
        self.boton_volver.place(x=500, y=600)

        self.boton_enviar=Button(nuevo, text="Agregar", command=self.crearTransaccion, font=("Helvetica", 13), activebackground='#78d6ff')
        self.boton_enviar.place(x=630, y=600)

    def cerrar_ventanaSecundaria(self):
        self.destroy()
        self.master.deiconify()

    def crearTransaccion(self):
        asunto=self.asunto_var.get()
        tipo="Ingreso"
        persona=self.persona_var.get()
        fecha=self.entrada3.get_date()
        medioPago=self.medioPago_var.get()
        ncheque=self.ncheque_var.get()
        monto=self.monto_var.get()
        descripcion=self.entrada6.get("1.0", "end-1c")
        numero=int(str(len(c.diccionario_ingresos)+1)+str(fecha.year))
        

        t=Transaccion(numero, asunto, tipo, persona, fecha, medioPago, ncheque, monto, descripcion)
        c.agregarIngreso(t, t.numero)
        self.cerrar_ventanaSecundaria()

#===============================VENTANA SECUNDARIA AGREGAR EGRESO==============================
class VentanaSecundariaAgregarEgreso(Frame):
    def __init__(self):
        nuevo=Frame.__init__(self)
        nuevo=Toplevel(self)
        nuevo.title("Agregar Egreso")
        nuevo.config(width=750, height=750)
        nuevo.resizable(width=False, height=False)
        
        self.asunto_var=StringVar()
        self.persona_var=StringVar()
        self.medioPago_var=StringVar()
        self.ncheque_var=StringVar()
        self.monto_var=StringVar()
        self.descripcion_var=StringVar()
        self.imprimir=BooleanVar()

        # Titulo
        self.titulo=Label(nuevo, text="Egreso", font=("Helvetica", 20))
        self.titulo.place(x=40, y=10)

        # Etiquetas
        self.etiqueta1=Label(nuevo, text="Asunto:", font=("Helvetica", 13))
        self.etiqueta1.place(x=40, y=60)

        self.etiqueta2=Label(nuevo, text="Enviado a:", font=("Helvetica", 13))
        self.etiqueta2.place(x=40, y=120)

        self.etiqueta3=Label(nuevo, text="Fecha:", font=("Helvetica", 13))
        self.etiqueta3.place(x=40, y=180)

        self.etiqueta4=Label(nuevo, text="N Cheque:", font=("Helvetica", 13))
        self.etiqueta4.place(x=40, y=300)

        self.etiqueta5=Label(nuevo, text="Monto:", font=("Helvetica", 13))
        self.etiqueta5.place(x=40, y=360)

        self.etiqueta6=Label(nuevo, text="Por concepto de:", font=("Helvetica", 13))
        self.etiqueta6.place(x=40, y=420)

        # Entradas
        self.entrada1=Entry(nuevo, textvariable=self.asunto_var, font=("Helvetica", 13))
        self.entrada1.place(x=200, y=60, width=500, height=32)

        self.entrada2=ttk.Combobox(nuevo, textvariable=self.persona_var, font=("Helvetica", 13))
        self.entrada2['values']=c.lista_enviado_a
        self.entrada2.place(x=200, y=120, width=500, height=32)

        self.entrada3=DateEntry(nuevo, width=50)
        self.entrada3.place(x=200, y=180, width=200, height=32)
        self.entrada3.config(headersbackground="#E62B0A", headersforeground="#ffffff", foreground="#000000", background="#ffffff")

        self.entrada4=Entry(nuevo, textvariable=self.ncheque_var, font=("Helvetica", 13))
        self.entrada4.place(x=200, y=300, width=500, height=32)

        self.entrada5=Entry(nuevo, textvariable=self.monto_var, font=("Helvetica", 13))
        self.entrada5.place(x=200, y=360, width=500, height=32)

        self.entrada6=scrolledtext.ScrolledText(nuevo, wrap=WORD, font=("Helvetica", 13))
        self.entrada6.place(x=200, y=420, width=500, height=118)

        # Botones radio
        self.radioBoton1=Radiobutton(nuevo, text="Cheque", font=("Helvetica", 13), variable=self.medioPago_var, value="Cheque")
        self.radioBoton1.place(x=200, y=240)
        self.radioBoton1.select()

        self.radioBoton2=Radiobutton(nuevo, text="Efectivo", font=("Helvetica", 13), variable=self.medioPago_var, value="Efectivo")
        self.radioBoton2.place(x=300, y=240)

        self.radioBoton3=Radiobutton(nuevo, text="Transferencia", font=("Helvetica", 13), variable=self.medioPago_var, value="Transferencia")
        self.radioBoton3.place(x=400, y=240)

        # CheckBox
        self.checkBox=Checkbutton(nuevo, text="¿Desea imprimir los datos del egreso en pdf?", variable=self.imprimir, onvalue=1, offvalue=0, font=("Helvetica", 12))
        self.checkBox.place(x=40, y=560)  

        # Botones
        self.boton_volver=Button(nuevo, text="Regresar", command=self.cerrar_ventanaSecundaria, font=("Helvetica", 13), activebackground='#78d6ff')
        self.boton_volver.place(x=500, y=600)

        self.boton_enviar=Button(nuevo, text="Agregar", command=self.crearTransaccion, font=("Helvetica", 13), activebackground='#78d6ff')
        self.boton_enviar.place(x=630, y=600)

    def cerrar_ventanaSecundaria(self):
        self.destroy()
        self.master.deiconify()

    def crearTransaccion(self):
        asunto=self.asunto_var.get()
        tipo="Egreso"
        persona=self.persona_var.get()
        fecha=self.entrada3.get_date()
        medioPago=self.medioPago_var.get()
        ncheque=self.ncheque_var.get()
        monto=self.monto_var.get()
        descripcion=self.entrada6.get("1.0", "end-1c")
        numero=int(str(len(c.diccionario_egresos)+1)+str(fecha.year))
        

        t=Transaccion(numero, asunto, tipo, persona, fecha, medioPago, ncheque, monto, descripcion)
        c.agregarEgreso(t, t.numero)
        self.cerrar_ventanaSecundaria()

#===============================VENTANA SECUNDARIA MOSTRAR LISTADO=============================
class VentanaSecundariaMostrarListado(Frame):
    def __init__(self):
        nuevo=Frame.__init__(self)
        nuevo=Toplevel(self)
        nuevo.title("Mostar Listado")
        nuevo.geometry("800x700")
        nuevo.resizable(width=False, height=False)

        #Boton
        boton_volver=Button(nuevo, text="Regresar", command=self.cerrar_ventanaSecundaria, font=("Arial", 12), activebackground='#78d6ff')
        boton_volver.place(x=210, y=600)

    def cerrar_ventanaSecundaria(self):
        self.destroy()
        self.master.deiconify()
    

app=Menu()
app.mainloop()
    