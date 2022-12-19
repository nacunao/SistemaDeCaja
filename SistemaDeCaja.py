from Contenedor import *
from Transaccion import *
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkcalendar import Calendar, DateEntry
from datetime import *

# Contenedor: contiene los diccionario de ingresos y egresos, la lista de enviado a/recido de
c = Contenedor()



#====================================VENTANA PRINCIPAL=========================================
class Menu(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Sistema de Caja")
        self.config(width=500, height=500)
        self.master.resizable(width=False, height=False)

        self.master.iconbitmap('abv_icon.ico')
        
        self.boton1=Button(self, text="Agregar Ingreso", command=self.abrir_ventanaSecundaria1, font=("Helvetica", 13), activebackground='#78d6ff')
        self.boton1.place(x=50, y=250,  height=50, width=400)

        self.boton2=Button(self, text="Agregar Egreso", command=self.abrir_ventanaSecundaria2, font=("Helvetica", 13), activebackground='#78d6ff')
        self.boton2.place(x=50, y=325,  height=50, width=400)

        self.boton3=Button(self,text="Mostrar Listado", command=self.abrir_ventanaSecundaria3, font=("Helvetica", 13), activebackground='#78d6ff')
        self.boton3.place(x=50, y=400, height=50, width=400)

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
        self.nuevo=Frame.__init__(self)
        self.nuevo=Toplevel(self)
        self.nuevo.title("Agregar Ingreso")
        self.nuevo.geometry("750x675")
        self.nuevo.resizable(width=False, height=False)
        self.nuevo.iconbitmap('abv_icon.ico')
        
        inicializar_variables(self)
        inicializar_titulo(self, "Ingreso")
        inicializar_etiquetas(self, "Ingreso", "Inicio")
        inicializar_entradas(self, "Ingreso", "Inicio")
        inicializar_radioBotones(self, "Ingreso")
        inicializar_checkBox(self)
        inicializar_botones(self, "Ingreso")


#===============================VENTANA SECUNDARIA AGREGAR EGRESO==============================
class VentanaSecundariaAgregarEgreso(Frame):
    def __init__(self):
        self.nuevo=Frame.__init__(self)
        self.nuevo=Toplevel(self)
        self.nuevo.title("Agregar Egreso")
        self.nuevo.geometry("750x675")
        self.nuevo.resizable(width=False, height=False)
        self.nuevo.iconbitmap('abv_icon.ico')
        
        inicializar_variables(self)
        inicializar_titulo(self, "Egreso")
        inicializar_etiquetas(self, "Egreso", "Inicio")
        inicializar_entradas(self, "Egreso", "Inicio")
        inicializar_radioBotones(self, "Egreso")
        inicializar_checkBox(self)
        inicializar_botones(self, "Egreso")


#================== Funciones de inicialización componentes ventanas secundarias agregar ingreso y agregar egreso ==================
def inicializar_variables(self):
    self.asunto_var=StringVar()
    self.persona_var=StringVar()
    self.personaNueva_var=StringVar()
    self.medioPago_var=StringVar()
    self.ncheque_var=StringVar()
    self.monto_var=StringVar()
    self.descripcion_var=StringVar()
    self.imprimir=BooleanVar()

def inicializar_titulo(self, t):
    # Titulo
    self.titulo=Label(self.nuevo, text=t, font=("Helvetica", 20))
    self.titulo.place(x=40, y=10)

def inicializar_etiquetas(self, t, medio):

    if medio=="Efectivo" or medio=="Transferencia":
        self.etiqueta4.destroy()
        self.etiqueta5.destroy()
        self.etiqueta6.destroy()

        self.etiqueta5=Label(self.nuevo, text="Monto:", font=("Helvetica", 13))
        self.etiqueta5.place(x=40, y=300)

        self.etiqueta6=Label(self.nuevo, text="Por concepto de:", font=("Helvetica", 13))
        self.etiqueta6.place(x=40, y=360)
        return
    
    if medio=="Cheque":
        self.etiqueta5.destroy()
        self.etiqueta6.destroy()

        self.etiqueta4=Label(self.nuevo, text="N Cheque:", font=("Helvetica", 13))
        self.etiqueta4.place(x=40, y=300)

        self.etiqueta5=Label(self.nuevo, text="Monto:", font=("Helvetica", 13))
        self.etiqueta5.place(x=40, y=360)

        self.etiqueta6=Label(self.nuevo, text="Por concepto de:", font=("Helvetica", 13))
        self.etiqueta6.place(x=40, y=420)
        return

    self.etiqueta1=Label(self.nuevo, text="Asunto:", font=("Helvetica", 13))
    self.etiqueta1.place(x=40, y=60)

    if t=="Ingreso":
        self.etiqueta2=Label(self.nuevo, text="Recibido de:", font=("Helvetica", 13))
    else: self.etiqueta2=Label(self.nuevo, text="Enviado a:", font=("Helvetica", 13))
    self.etiqueta2.place(x=40, y=120)

    self.etiqueta3=Label(self.nuevo, text="Fecha:", font=("Helvetica", 13))
    self.etiqueta3.place(x=40, y=180)

    self.etiqueta4=Label(self.nuevo, text="N Cheque:", font=("Helvetica", 13))
    self.etiqueta4.place(x=40, y=300)

    self.etiqueta5=Label(self.nuevo, text="Monto:", font=("Helvetica", 13))
    self.etiqueta5.place(x=40, y=360)

    self.etiqueta6=Label(self.nuevo, text="Por concepto de:", font=("Helvetica", 13))
    self.etiqueta6.place(x=40, y=420) 

    

def inicializar_entradas(self, t, medio):

    if medio=="Efectivo" or medio=="Transferencia":
        self.entrada4.destroy()
        self.entrada5.destroy()
        self.entrada6.destroy()
        self.barra_de_desplazamiento.destroy()

        self.entrada5=Entry(self.nuevo, textvariable=self.monto_var, font=("Helvetica", 13))
        self.entrada5.place(x=200, y=300, width=500, height=32)

        self.barra_de_desplazamiento=Scrollbar(self.nuevo)
        self.barra_de_desplazamiento.place(x=700, y=360, height=118)
        self.entrada6=Text(self.nuevo, wrap=WORD, font=("Helvetica", 13), yscrollcommand = self.barra_de_desplazamiento.set)
        self.entrada6.place(x=200, y=360, width=500, height=118)
        self.barra_de_desplazamiento.config(command=self.entrada6.yview)
        return

    if medio=="Cheque":
        self.entrada5.destroy()
        self.entrada6.destroy()
        self.barra_de_desplazamiento.destroy()

        self.entrada4=Entry(self.nuevo, textvariable=self.ncheque_var, font=("Helvetica", 13))
        self.entrada4.place(x=200, y=300, width=500, height=32)

        self.entrada5=Entry(self.nuevo, textvariable=self.monto_var, font=("Helvetica", 13))
        self.entrada5.place(x=200, y=360, width=500, height=32)

        self.barra_de_desplazamiento=Scrollbar(self.nuevo)
        self.barra_de_desplazamiento.place(x=700, y=420, height=118)
        self.entrada6=Text(self.nuevo, wrap=WORD, font=("Helvetica", 13), yscrollcommand = self.barra_de_desplazamiento.set)
        self.entrada6.place(x=200, y=420, width=500, height=118)
        self.barra_de_desplazamiento.config(command=self.entrada6.yview)
        return

    def comboboxclick(event):
        self.entrada2_adicional=Entry(self.nuevo, textvariable=self.personaNueva_var, font=("Helvetica", 13))
        self.entrada2_adicional.place(x=455, y=120, width=245, height=32)
        if self.persona_var.get() !='nuevo':
            self.entrada2_adicional.config(state=DISABLED)
        else:
            self.entrada2_adicional.config(state=NORMAL)

    # Entradas
    self.entrada1=Entry(self.nuevo, textvariable=self.asunto_var, font=("Helvetica", 13))
    self.entrada1.place(x=200, y=60, width=500, height=32)

    self.entrada2=ttk.Combobox(self.nuevo, textvariable=self.persona_var, font=("Helvetica", 13))
    if t=="Ingreso":
        c.agregarRecibidoDe('nuevo')
        self.entrada2['values']=c.lista_recibido_de
    else:
        c.agregarEnviadoA('nuevo')
        self.entrada2['values']=c.lista_enviado_a
    self.entrada2.bind("<<ComboboxSelected>>", comboboxclick)
    self.entrada2.place(x=200, y=120, width=245, height=32)

    self.entrada3=DateEntry(self.nuevo, width=50)
    self.entrada3.place(x=200, y=180, width=200, height=32)
    self.entrada3.config(headersbackground="#E62B0A", headersforeground="#ffffff", foreground="#000000", background="#ffffff")

    self.entrada4=Entry(self.nuevo, textvariable=self.ncheque_var, font=("Helvetica", 13))
    self.entrada4.place(x=200, y=300, width=500, height=32)

    self.entrada5=Entry(self.nuevo, textvariable=self.monto_var, font=("Helvetica", 13))
    self.entrada5.place(x=200, y=360, width=500, height=32)

    self.barra_de_desplazamiento=Scrollbar(self.nuevo)
    self.barra_de_desplazamiento.place(x=700, y=420, height=118)
    self.entrada6=Text(self.nuevo, wrap=WORD, font=("Helvetica", 13), yscrollcommand = self.barra_de_desplazamiento.set)
    self.entrada6.place(x=200, y=420, width=500, height=118)
    self.barra_de_desplazamiento.config(command=self.entrada6.yview)


def inicializar_radioBotones(self, t):
    # Botones radio
    self.radioBoton1=Radiobutton(self.nuevo, text="Cheque", font=("Helvetica", 13), variable=self.medioPago_var, value="Cheque", command=lambda:mostrar_ncheque(self, t, "Cheque"))
    self.radioBoton1.place(x=200, y=240)
    self.radioBoton1.select()

    self.radioBoton2=Radiobutton(self.nuevo, text="Efectivo", font=("Helvetica", 13), variable=self.medioPago_var, value="Efectivo", command=lambda:ocultar_ncheque(self, t, "Efectivo"))
    self.radioBoton2.place(x=300, y=240)
    
    self.radioBoton3=Radiobutton(self.nuevo, text="Transferencia", font=("Helvetica", 13), variable=self.medioPago_var, value="Transferencia", command=lambda:ocultar_ncheque(self, t, "Transferencia"))
    self.radioBoton3.place(x=400, y=240)

def inicializar_checkBox(self):
    # CheckBox
    self.checkBox=Checkbutton(self.nuevo, text="¿Desea imprimir los datos del ingreso en pdf?", variable=self.imprimir, onvalue=1, offvalue=0, font=("Helvetica", 12))
    self.checkBox.place(x=40, y=560)  

def inicializar_botones(self, tipo):
    # Botones
    self.boton_volver=Button(self.nuevo, text="Regresar", command=lambda:cerrar_ventanaSecundaria(self), font=("Helvetica", 13), activebackground='#78d6ff')
    self.boton_volver.place(x=500, y=600)

    self.boton_enviar=Button(self.nuevo, text="Agregar", command=lambda:crearTransaccion(self, tipo), font=("Helvetica", 13), activebackground='#78d6ff')
    self.boton_enviar.place(x=630, y=600)

def ocultar_ncheque(self, t, medio):
    inicializar_etiquetas(self, t, medio)
    inicializar_entradas(self, t, medio)

def mostrar_ncheque(self, t, medio):
    inicializar_etiquetas(self, t, medio)
    inicializar_entradas(self, t, medio)

def crearTransaccion(self, tipo):
    asunto=self.asunto_var.get()
    persona=self.persona_var.get()
    if persona=='nuevo':
        persona=self.personaNueva_var.get()
    fecha=self.entrada3.get_date()
    medioPago=self.medioPago_var.get()
    if medioPago=="Cheque":
        ncheque=str(self.ncheque_var.get())
    else: ncheque=0
    monto=str(self.monto_var.get())
    descripcion=self.entrada6.get("1.0", "end-1c")
    if tipo=="Ingreso":
        numero=int(str(len(c.diccionario_ingresos)+1)+str(fecha.year))
    else: numero=int(str(len(c.diccionario_egresos)+1)+str(fecha.year))
    

    t=Transaccion(numero, asunto, tipo, persona, fecha, medioPago, ncheque, monto, descripcion)
    if tipo=="Ingreso":
        c.agregarIngreso(t, t.numero)
        c.agregarRecibidoDe(persona)
    else:
        c.agregarEgreso(t, t.numero)
        c.agregarEnviadoA(persona)
    cerrar_ventanaSecundaria(self)



#===============================VENTANA SECUNDARIA MOSTRAR LISTADO=============================
class VentanaSecundariaMostrarListado(Frame):
    def __init__(self):
        self.nuevo=Frame.__init__(self)
        self.nuevo=Toplevel(self)
        self.nuevo.title("Mostar Listado")
        self.nuevo.geometry("1000x650")
        self.nuevo.resizable(width=False, height=False)
        self.nuevo.iconbitmap('abv_icon.ico')

        
        self.barra1=Scrollbar(self.nuevo, orient=HORIZONTAL)
        self.barra1.place(x=40, y=490, width=920)
        self.barra2=Scrollbar(self.nuevo, orient=VERTICAL)
        self.barra2.place(x=960, y=40, height=500)
        columnas=("Ingreso/Egreso", "Número Folio", "Asunto", "Recibido de/Enviado a", "Fecha", "Medio", "Número de Cheque", "Monto", "Descripción")
        self.tabla = ttk.Treeview(self.nuevo, columns=columnas, selectmode="extended", xscrollcommand=self.barra1, yscrollcommand=self.barra2)
        
        self.barra1.config(command=self.tabla.xview)
        self.barra2.config(command=self.tabla.yview)
        
        
        
        self.tabla.heading('Ingreso/Egreso', text="Ingreso/Egreso",anchor=W)
        self.tabla.heading('Número Folio', text="Número Folio",anchor=W)
        self.tabla.heading('Asunto', text="Asunto",anchor=W)
        self.tabla.heading('Recibido de/Enviado a', text="Recibido de/Enviado a",anchor=W)
        self.tabla.heading('Fecha', text="Fecha",anchor=W)
        self.tabla.heading('Medio', text="Medio",anchor=W)
        self.tabla.heading('Número de Cheque', text="Número de Cheque",anchor=W)
        self.tabla.heading('Monto', text="Monto",anchor=W)
        self.tabla.heading('Descripción', text="Por concepto de",anchor=W)
        self.tabla.column('#0', stretch=NO, minwidth=0,width=0)
        self.tabla.column('#1', stretch=NO, minwidth=300, width=300)
        self.tabla.column('#2', stretch=NO, minwidth=300, width=300)
        self.tabla.column('#3', stretch=NO, minwidth=300, width=300)
        self.tabla.column('#4', stretch=NO, minwidth=300, width=300)
        self.tabla.column('#5', stretch=NO, minwidth=300, width=300)
        self.tabla.column('#6', stretch=NO, minwidth=300, width=300)
        self.tabla.column('#7', stretch=NO, minwidth=300, width=300)
        self.tabla.column('#8', stretch=NO, minwidth=300, width=300)
        self.tabla.column('#9', stretch=NO, minwidth=300, width=300)
        self.tabla.place(x=40, y=40, width=920, height=500)


        #Boton
        boton_volver=Button(self.nuevo, text="Regresar", command=lambda:cerrar_ventanaSecundaria(self), font=("Arial", 12), activebackground='#78d6ff')
        boton_volver.place(x=900, y=600)


def cerrar_ventanaSecundaria(self):
    c.eliminarRecibidoDe('nuevo')
    c.eliminarEnviadoA('nuevo')
    self.destroy()
    self.master.deiconify()

app=Menu()
app.mainloop()