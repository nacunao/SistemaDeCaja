from Contenedor import *
from Transaccion import *
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import *

c = Contenedor()

class Menu(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Menu")
        self.config(width=500, height=500)
        self.master.resizable(width=False, height=False)

        
        self.boton1=Button(self, text="Agregar Ingreso", command=self.abrir_ventanaSecundaria1, activebackground='#78d6ff')
        self.boton1.place(x=150, y=50,  height=30, width=150)

        self.boton2=Button(self, text="Agregar Egreso", command=self.abrir_ventanaSecundaria2, activebackground='#78d6ff')
        self.boton2.place(x=150, y=150,  height=30, width=150)

        self.boton3=Button(self,text="Mostrar Listado", command=self.abrir_ventanaSecundaria3, activebackground='#78d6ff')
        self.boton3.place(x=150, y=250, height=30, width=150)

    def abrir_ventanaSecundaria1(self):
        self.master.withdraw()
        self.nuevaVentana=VentanaSecundariaAgregarIngreso()

    def abrir_ventanaSecundaria2(self):
        self.master.withdraw()
        self.nuevaVentana=VentanaSecundariaAgregarEgreso()

    def abrir_ventanaSecundaria3(self):
        self.master.withdraw()
        self.nuevaVentana=VentanaSecundariaMostrarListado()

class VentanaSecundariaAgregarIngreso(Frame):
    def __init__(self):
        nuevo=Frame.__init__(self)
        nuevo=Toplevel(self)
        nuevo.title("Agregar Ingreso")
        nuevo.geometry("800x700")
        nuevo.resizable(width=False, height=False)
        
        self.asunto_var=StringVar()
        self.persona_var=StringVar()
        self.ncheque_var=StringVar()
        self.efectivo_var=StringVar()
        self.descripcion_var=StringVar()

        # Titulo
        titulo=Label(nuevo, text="Ingreso", font=("Arial", 18))
        titulo.place(x=40, y=10)



        #Etiquetas
        etiqueta1=Label(nuevo, text="Asunto:", font=("Arial", 12))
        etiqueta1.place(x=40, y=60)
        etiqueta2=Label(nuevo, text="Recibido de:", font=("Arial", 12))
        etiqueta2.place(x=40, y=120)
        etiqueta3=Label(nuevo, text="Fecha:", font=("Arial", 12))
        etiqueta3.place(x=40, y=180)
        etiqueta4=Label(nuevo, text="N Cheque:", font=("Arial", 12))
        etiqueta4.place(x=40, y=240)
        etiqueta5=Label(nuevo, text="Efectivo:", font=("Arial", 12))
        etiqueta5.place(x=40, y=300)
        etiqueta6=Label(nuevo, text="Por concepto de:", font=("Arial", 12))
        etiqueta6.place(x=40, y=360)

        #Entradas
        entrada1=Entry(nuevo, textvariable=self.asunto_var)
        entrada1.place(x=200, y=60, width=500, height=32)

        self.entrada2=ttk.Combobox(nuevo, textvariable=self.persona_var, width=15)
        self.entrada2['values']=("Asunto 1", "Asunto 2", "Asunto 3")
        self.entrada2.place(x=200, y=120)

        self.entrada3=DateEntry(nuevo, width=50)
        self.entrada3.place(x=200, y=180, width=200, height=32)
        self.entrada3.config(headersbackground="#364c55", headersforeground="#ffffff", foreground="#000000", background="#ffffff")


        entrada4=Entry(nuevo, textvariable=self.ncheque_var)
        entrada4.place(x=200, y=240, width=500, height=32)
        entrada5=Entry(nuevo, textvariable=self.efectivo_var)
        entrada5.place(x=200, y=300, width=500, height=32)
        entrada6=Entry(nuevo,textvariable=self.descripcion_var)
        entrada6.place(x=200, y=360, width=500, height=32)

        #Botones
        boton_volver=Button(nuevo, text="Regresar", command=self.cerrar_ventanaSecundaria, font=("Arial", 12), activebackground='#78d6ff')
        boton_volver.place(x=210, y=600)

        boton_enviar=Button(nuevo, text="Agregar", command=self.crearTransaccion, font=("Arial", 12), activebackground='#78d6ff')
        boton_enviar.place(x=300, y=600)

    def cerrar_ventanaSecundaria(self):
        self.destroy()
        self.master.deiconify()

    def crearTransaccion(self):
        numero=len(c.diccionario_transacciones)+1
        asunto=self.asunto_var.get()
        tipo="Ingreso"
        persona=self.persona_var.get()
        fecha=self.entrada3.get_date()
        ncheque=self.ncheque_var.get()
        efectivo=self.efectivo_var.get()
        descripcion=self.descripcion_var.get()

        t=Transaccion(numero, asunto, tipo, persona, fecha, ncheque, efectivo, descripcion)
        c.agregarTransaccion(t, t.numero)
        self.cerrar_ventanaSecundaria()

class VentanaSecundariaAgregarEgreso(Frame):
    def __init__(self):
        nuevo=Frame.__init__(self)
        nuevo=Toplevel(self)
        nuevo.title("Agregar Egreso")
        nuevo.geometry("800x700")
        nuevo.resizable(width=False, height=False)
        
        self.asunto_var=StringVar()
        self.persona_var=StringVar()
        self.ncheque_var=StringVar()
        self.efectivo_var=StringVar()
        self.descripcion_var=StringVar()

        # Titulo
        titulo=Label(nuevo, text="Egreso", font=("Arial", 18))
        titulo.place(x=40, y=10)



        #Etiquetas
        etiqueta1=Label(nuevo, text="Asunto:", font=("Arial", 12))
        etiqueta1.place(x=40, y=60)
        etiqueta2=Label(nuevo, text="Enviado a:", font=("Arial", 12))
        etiqueta2.place(x=40, y=120)
        etiqueta3=Label(nuevo, text="Fecha:", font=("Arial", 12))
        etiqueta3.place(x=40, y=180)
        etiqueta4=Label(nuevo, text="N Cheque:", font=("Arial", 12))
        etiqueta4.place(x=40, y=240)
        etiqueta5=Label(nuevo, text="Efectivo:", font=("Arial", 12))
        etiqueta5.place(x=40, y=300)
        etiqueta6=Label(nuevo, text="Por concepto de:", font=("Arial", 12))
        etiqueta6.place(x=40, y=360)

        #Entradas
        entrada1=Entry(nuevo, textvariable=self.asunto_var)
        entrada1.place(x=200, y=60, width=500, height=32)
        
        self.entrada2=ttk.Combobox(nuevo, textvariable=self.persona_var, width=15)
        self.entrada2['values']=("Asunto 1", "Asunto 2", "Asunto 3")
        self.entrada2.place(x=200, y=120)

        self.entrada3=DateEntry(nuevo, width=50)
        self.entrada3.place(x=200, y=180, width=200, height=32)
        self.entrada3.config(headersbackground="#364c55", headersforeground="#ffffff", foreground="#000000", background="#ffffff")


        entrada4=Entry(nuevo, textvariable=self.ncheque_var)
        entrada4.place(x=200, y=240, width=500, height=32)
        entrada5=Entry(nuevo, textvariable=self.efectivo_var)
        entrada5.place(x=200, y=300, width=500, height=32)
        entrada6=Entry(nuevo,textvariable=self.descripcion_var)
        entrada6.place(x=200, y=360, width=500, height=32)

        #Botones
        boton_volver=Button(nuevo, text="Regresar", command=self.cerrar_ventanaSecundaria, font=("Arial", 12), activebackground='#78d6ff')
        boton_volver.place(x=210, y=600)

        boton_enviar=Button(nuevo, text="Agregar", command=self.crearTransaccion, font=("Arial", 12), activebackground='#78d6ff')
        boton_enviar.place(x=300, y=600)

    def cerrar_ventanaSecundaria(self):
        self.destroy()
        self.master.deiconify()

    def crearTransaccion(self):
        numero=len(c.diccionario_transacciones)+1
        asunto=self.asunto_var.get()
        tipo="Egreso"
        persona=self.persona_var.get()
        fecha=self.entrada3.get_date()
        ncheque=self.ncheque_var.get()
        efectivo=self.efectivo_var.get()
        descripcion=self.descripcion_var.get()

        t=Transaccion(numero, asunto, tipo, persona, fecha, ncheque, efectivo, descripcion)
        c.agregarTransaccion(t, t.numero)
        print(c.diccionario_transacciones[t.numero].fecha)
        self.cerrar_ventanaSecundaria()

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
    