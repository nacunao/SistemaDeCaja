from Contenedor import *

from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import *

import mysql.connector

# Conexión a la base de datos remota
def conectar_BaseDeDatos(opcion):
    conexion_bdd = mysql.connector.connect(user='hpn9tpk1dry0lmzu7377', password='pscale_pw_z8FWTgp8gcRZJUEmtlO1GTY2mep54VHI46hlq7lxyOm',
                                    host='us-east.connect.psdb.cloud',
                                    database='administracion-ingresos-egresos')
    
    # Importar la base de datos
    if opcion==1:
        mycursor = conexion_bdd.cursor()
        mycursor.execute("SELECT * FROM Transaccion")
        fila = mycursor.fetchall()

        for dato in fila:
            print(dato[0])
            tabla.insert('', 'end', values=(dato[0], dato[1], dato[2], dato[3], dato[4], dato[5], dato[6], dato[7], dato[8]))
    
    # Agregar elemento a la base de datos
    elif opcion==2:
        mycursor=conexion_bdd.cursor()
        mycursor.execute("SELECT COUNT(*) FROM Transaccion WHERE CAST(numero AS CHAR(10)) LIKE '%"+str(fecha.year)+"' AND `tipo` LIKE '"+str(tipo)+"'")
        fila = mycursor.fetchall()
        numero = int(str(int(fila[0][0])+1)+str(fecha.year))

        sql = "INSERT INTO Transaccion (numero, tipo, asunto, persona, fecha, medio, nCheque, monto, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (numero, tipo, asunto, persona, date.isoformat(fecha), medio, ncheque, monto, descripcion)


        mycursor = conexion_bdd.cursor()
        mycursor.execute(sql, valores)
        conexion_bdd.commit()

    # Buscar en la base de datos por persona (Recibido de:/Enviado a:)
    elif opcion==3:
        if busqueda_var.get() != "":
            tabla.delete(*tabla.get_children())
            mycursor = conexion_bdd.cursor()
            mycursor.execute("SELECT * FROM Transaccion WHERE `persona` LIKE '%"+busqueda_var.get()+"%'")
            fila = mycursor.fetchall()
            for dato in fila:
                tabla.insert('', 'end', values=(dato[0], dato[1], dato[2], dato[3], dato[4], dato[5], dato[6], dato[7], dato[8]))
    
    # Limpiar busqueda de la base de datos
    else:
        tabla.delete(*tabla.get_children())
        mycursor = conexion_bdd.cursor()
        mycursor.execute("SELECT * FROM Transaccion")
        fila = mycursor.fetchall()

        for dato in fila:
            print(dato[0])
            tabla.insert('', 'end', values=(dato[0], dato[1], dato[2], dato[3], dato[4], dato[5], dato[6], dato[7], dato[8]))
            
    conexion_bdd.close()

c = Contenedor()

#====================================VENTANA PRINCIPAL=========================================
class Aplicacion(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Sistema de Caja")
        width = 1200
        height = 675
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.master.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.master.resizable(width=False, height=False)
        self.master.configure(bg='#FFFFFF')

        self.master.iconbitmap('abv_icon.ico')

        # Label Frames
        contenedor1=LabelFrame(self.master, text="Buscador Persona", bg='#8297BC', fg='#FFFFFF')
        contenedor1.place(x=40, y=10, width=575, height=75)
        contenedor2=LabelFrame(self.master, text="Operaciones", bg='#E64611', fg='#FFFFFF')
        contenedor2.place(x=40, y=580, width=375, height=75)
        contenedorTabla=Label(self.master, text="Base de datos", bg='#EDB712', fg='#FFFFFF')
        contenedorTabla.place(x=40, y=120, width=1120, height=420)
        
        # Tabla
        global tabla
        global barra1
        global barra2
        barra1=Scrollbar(contenedorTabla, orient=HORIZONTAL)
        barra1.pack(side=BOTTOM, fill=X)
        barra2=Scrollbar(contenedorTabla, orient=VERTICAL)
        barra2.pack(side=RIGHT, fill=Y)
        tabla = ttk.Treeview(contenedorTabla, selectmode='extend', xscrollcommand=barra1, yscrollcommand=barra2)
        tabla.place(x=10, y=10, width=1080, height=380)
        tabla['columns']=("1", "2", "3", "4", "5", "6", "7", "8", "9")
        tabla['show']='headings'
        
        barra1.config(command=tabla.xview)
        barra2.config(command=tabla.yview)
        
        tabla.column('1', minwidth=80, width=80)
        tabla.column('2', minwidth=100, width=100)
        tabla.column('3', minwidth=300, width=300)
        tabla.column('4', minwidth=300, width=300)
        tabla.column('5', minwidth=80, width=80)
        tabla.column('6', minwidth=80, width=80)
        tabla.column('7', minwidth=300, width=300)
        tabla.column('8', minwidth=100, width=100)
        tabla.column('9', minwidth=300, width=300)

        tabla.heading('1', text="Número",anchor=W)
        tabla.heading('2', text="Tipo",anchor=W)
        tabla.heading('3', text="Asunto",anchor=W)
        tabla.heading('4', text="Recibido de/Enviado a",anchor=W)
        tabla.heading('5', text="Fecha",anchor=W)
        tabla.heading('6', text="Medio",anchor=W)
        tabla.heading('7', text="Número de Cheque",anchor=W)
        tabla.heading('8', text="Monto",anchor=W)
        tabla.heading('9', text="Por concepto de",anchor=W)

        # Conexión con la base de datos (importación de datos)
        conectar_BaseDeDatos(1)

        global busqueda_var
        busqueda_var=StringVar()

        def habilitar_boton(evento):
            if len(entrada1.get())>0:
                boton1['state']=NORMAL
            else: boton1['state']=DISABLED
        # Entradas
        entrada1=Entry(contenedor1, textvariable=busqueda_var)
        entrada1.place(x=20, y=10, width=350, height=32)
        self.master.bind('<KeyRelease>', habilitar_boton)

        # Botones
        boton1=Button(contenedor1, text="Buscar", command=self.buscar_persona, font=("Helvetica", 12), bg='#FFFFFF')
        boton1.place(x=400, y=10)
        boton1['state']=DISABLED
        boton2=Button(contenedor1, text="Limpiar", command=self.limpiar_tabla, font=("Helvetica", 12), bg='#FFFFFF')
        boton2.place(x=475, y=10)
        boton3=Button(contenedor2, text="Agregar Ingreso", command=self.abrir_ventanaSecundaria1, font=("Helvetica", 12))
        boton3.place(x=20, y=10)
        boton4=Button(contenedor2, text="Agregar Egreso", command=self.abrir_ventanaSecundaria2, font=("Helvetica", 12))
        boton4.place(x=220, y=10)



    def abrir_ventanaSecundaria1(self):
        self.master.withdraw()
        self.nuevaVentana=VentanaSecundariaAgregarIngreso()

    def abrir_ventanaSecundaria2(self):
        self.master.withdraw()
        self.nuevaVentana=VentanaSecundariaAgregarEgreso()
    
    def buscar_persona(self):
        conectar_BaseDeDatos(3)

    def limpiar_tabla(self):
        conectar_BaseDeDatos(4)

#=================================VENTANA SECUNDARIA AGREGAR INGRESO===========================
class VentanaSecundariaAgregarIngreso(Frame):
    def __init__(self):
        self.nuevo=Frame.__init__(self)
        self.nuevo=Toplevel(self)
        self.nuevo.configure(bg='#FFFFFF')
        self.nuevo.title("Agregar Ingreso")
        self.nuevo.geometry("760x660")
        self.nuevo.resizable(width=False, height=False)
        self.nuevo.iconbitmap('abv_icon.ico')
        
        inicializar_variables(self)
        inicializar_radioBotones(self)
        inicializar_componentes(self, "Ingreso", "Inicio")


#===============================VENTANA SECUNDARIA AGREGAR EGRESO==============================
class VentanaSecundariaAgregarEgreso(Frame):
    def __init__(self):
        self.nuevo=Frame.__init__(self)
        self.nuevo=Toplevel(self)
        self.nuevo.configure(bg='#FFFFFF')
        self.nuevo.title("Agregar Egreso")
        self.nuevo.geometry("760x660")
        self.nuevo.resizable(width=False, height=False)
        self.nuevo.iconbitmap('abv_icon.ico')
        
        inicializar_variables(self)
        inicializar_radioBotones(self)
        inicializar_componentes(self, "Egreso", "Inicio")
        


#================== Funciones de inicialización componentes ventanas secundarias agregar ingreso y agregar egreso ==================
def inicializar_variables(self):
    self.asunto_var=StringVar()
    self.persona_var=StringVar()
    self.personaNueva_var=StringVar() 
    self.medio_var=StringVar()
    self.ncheque_var=StringVar()
    self.monto_var=StringVar()
    self.descripcion_var=StringVar()
    self.imprimir=BooleanVar()




def inicializar_componentes(self, tipo, medio):
    # Validación entradas solo números
    def validacion_numeros(entrada):
        return entrada.isdigit()

    validacionNumero=self.nuevo.register(validacion_numeros)

    # Validación entradas vacias
    def validacion_vacia(evento):
        if medio=='Inicio' or medio=='Cheque':
            if self.entrada2.get()=='nuevo':
                if len(self.entrada1.get())>0 and len(self.entrada2_adicional.get())>0 and len(self.entrada4.get())>0 and len(self.entrada5.get())>0 and len(self.entrada6.get("1.0", "end-1c")):
                    self.boton2['state']=NORMAL
                else: self.boton2['state']=DISABLED
            else:
                if len(self.entrada1.get())>0 and len(self.entrada2.get())>0 and len(self.entrada4.get())>0 and len(self.entrada5.get())>0 and len(self.entrada6.get("1.0", "end-1c")):
                    self.boton2['state']=NORMAL
                else: self.boton2['state']=DISABLED
        else:
            if self.entrada2.get()=='nuevo':
                if len(self.entrada1.get())>0 and len(self.entrada2_adicional.get())>0 and len(self.entrada5.get())>0 and len(self.entrada6.get("1.0", "end-1c")):
                    self.boton2['state']=NORMAL
                else: self.boton2['state']=DISABLED
            else:
                if len(self.entrada1.get())>0 and len(self.entrada2.get())>0 and len(self.entrada5.get())>0 and len(self.entrada6.get("1.0", "end-1c")):
                    self.boton2['state']=NORMAL
                else: self.boton2['state']=DISABLED

    self.nuevo.bind('<KeyRelease>', validacion_vacia)

    if medio=='Inicio':

        # Titulo
        self.titulo=Label(self.nuevo, text=tipo, font=("Helvetica", 18))
        self.titulo.configure(bg='#FFFFFF')
        self.titulo.place(x=40, y=10)

        # Label Frame
        self.contenedor1=LabelFrame(self.nuevo, text="Asunto", font=("Helvetica", 12), bg='#D4CDD6', fg='#02020D')
        self.contenedor1.place(x=40, y=50, width=680, height=65)

        if tipo=='Ingreso':
            self.contenedor2=LabelFrame(self.nuevo, text="Recibido de", font=("Helvetica", 12), bg='#D4CDD6', fg='#02020D')
        else: self.contenedor2=LabelFrame(self.nuevo, text="Enviado a", font=("Helvetica", 12), bg='#D4CDD6', fg='#02020D')
        self.contenedor2.place(x=40, y=120, width=680, height=65)

        self.contenedor3=LabelFrame(self.nuevo, text="Fecha", font=("Helvetica", 12), bg='#D4CDD6', fg='#02020D')
        self.contenedor3.place(x=40, y=190, width=680, height=65)

        self.contenedor4=LabelFrame(self.nuevo, text="Número de Cheque", font=("Helvetica", 12), bg='#D4CDD6', fg='#02020D')
        self.contenedor4.place(x=400, y=260, width=320, height=65)

        self.contenedor5=LabelFrame(self.nuevo, text="Monto", font=("Helvetica", 12), bg='#D4CDD6', fg='#02020D')
        self.contenedor5.place(x=40, y=330, width=680, height=65)

        self.contenedor6=LabelFrame(self.nuevo, text="Por concepto de", font=("Helvetica", 12), bg='#D4CDD6', fg='#02020D')
        self.contenedor6.place(x=40, y=400, width=680, height=150)

        # Entradas
        def comboboxclick(event):
            self.entrada2_adicional=Entry(self.contenedor2, textvariable=self.personaNueva_var, font=("Helvetica", 13))
            self.entrada2_adicional.place(x=330, y=5, width=310, height=32)
            if self.persona_var.get() !='nuevo':
                self.entrada2_adicional.config(state=DISABLED)
            else:
                self.entrada2_adicional.config(state=NORMAL)

        self.entrada1=Entry(self.contenedor1, textvariable=self.asunto_var, font=("Helvetica", 13))
        self.entrada1.place(x=10, y=5, width=660, height=32)

        self.entrada2=ttk.Combobox(self.contenedor2, textvariable=self.persona_var, font=("Helvetica", 13))
        if tipo=="Ingreso":
            c.agregarRecibidoDe('nuevo')
            self.entrada2['values']=c.lista_recibido_de
        else:
            c.agregarEnviadoA('nuevo')
            self.entrada2['values']=c.lista_enviado_a
        self.entrada2.bind("<<ComboboxSelected>>", comboboxclick)
        self.entrada2.place(x=10, y=5, width=310, height=32)

        self.entrada3=DateEntry(self.contenedor3, width=50)
        self.entrada3.place(x=10, y=5, width=310, height=32)
        self.entrada3.config(headersbackground="#E62B0A", headersforeground="#ffffff", foreground="#000000", background="#ffffff")

        self.entrada4=Entry(self.contenedor4, textvariable=self.ncheque_var, font=("Helvetica", 13), validate="key", validatecommand=(validacionNumero, '%S'))
        self.entrada4.place(x=10, y=5, width=300, height=32)

        self.entrada5=Entry(self.contenedor5, textvariable=self.monto_var, font=("Helvetica", 13), validate="key", validatecommand=(validacionNumero, '%S'))
        self.entrada5.place(x=10, y=5, width=660, height=32)

        self.barra1=Scrollbar(self.contenedor6)
        self.barra1.place(x=650, y=5, height=110)
        self.entrada6=Text(self.contenedor6, wrap=WORD, font=("Helvetica", 13), yscrollcommand = self.barra1.set)
        self.entrada6.place(x=10, y=5, width=635, height=110)
        self.barra1.config(command=self.entrada6.yview)



        # CheckBox
        self.checkBox=Checkbutton(self.nuevo, text="¿Desea imprimir los datos del "+tipo+" en pdf?", variable=self.imprimir, onvalue=1, offvalue=0, font=("Helvetica", 12))
        self.checkBox.configure(bg='#FFFFFF')
        self.checkBox.place(x=40, y=600)

        # Botones
        self.boton1=Button(self.nuevo, text="Regresar", command=lambda:cerrar_ventanaSecundaria(self), font=("Helvetica", 13))
        self.boton1.configure(bg='#FFD1A5')
        self.boton1.place(x=500, y=600)

        self.boton2=Button(self.nuevo, text="Agregar", command=lambda:crearTransaccion(self, tipo), font=("Helvetica", 13))
        self.boton2.configure(bg='#FFD1A5')
        self.boton2.place(x=630, y=600)
        self.boton2['state']=DISABLED
    
    elif medio=='Cheque':
        self.contenedor4.destroy()

        self.contenedor4=LabelFrame(self.nuevo, text="Número de Cheque", font=("Helvetica", 12), bg='#D4CDD6', fg='#02020D')
        self.contenedor4.place(x=400, y=260, width=320, height=65)

        self.entrada4=Entry(self.contenedor4, textvariable=self.ncheque_var, font=("Helvetica", 13), validate="key", validatecommand=(validacionNumero, '%S'))
        self.entrada4.place(x=10, y=5, width=300, height=32)
    
    else:
        self.contenedor4.destroy()


def inicializar_radioBotones(self):
    # Label Frame
    contenedorRB=LabelFrame(self.nuevo, text="Medio", font=("Helvetica", 12), bg='#D4CDD6', fg='#02020D')
    contenedorRB.place(x=40, y=260, width=350, height=65)


    # Botones radio
    radioBoton1=Radiobutton(contenedorRB, text="Cheque", font=("Helvetica", 13), variable=self.medio_var, value="Cheque", command=lambda:inicializar_componentes(self, "", "Cheque"), bg='#FFFFFF')
    radioBoton1.place(x=5, y=5)
    radioBoton1.select()

    radioBoton2=Radiobutton(contenedorRB, text="Efectivo", font=("Helvetica", 13), variable=self.medio_var, value="Efectivo", command=lambda:inicializar_componentes(self, "","Efectivo"), bg='#FFFFFF')
    radioBoton2.place(x=100, y=5)
    
    radioBoton3=Radiobutton(contenedorRB, text="Transferencia", font=("Helvetica", 13), variable=self.medio_var, value="Transferencia", command=lambda:inicializar_componentes(self, "", "Transferencia"), bg='#FFFFFF')
    radioBoton3.place(x=200, y=5)

    
def crearTransaccion(self, t):
    global numero
    global tipo
    global asunto
    global persona
    global fecha
    global medio
    global ncheque
    global monto
    global descripcion
    asunto=self.entrada1.get()
    persona=self.entrada2.get()
    if persona=='nuevo':
        persona=self.entrada2_adicional.get()
    fecha=self.entrada3.get_date()
    medio=self.medio_var.get()
    if medio=="Cheque":
        ncheque=int(self.entrada4.get())
    else: ncheque=0
    monto=int(self.entrada5.get())
    descripcion=self.entrada6.get("1.0", "end-1c")
    tipo=t
    
    conectar_BaseDeDatos(2)
    cerrar_ventanaSecundaria(self)


def cerrar_ventanaSecundaria(self):
    c.eliminarRecibidoDe('nuevo')
    c.eliminarEnviadoA('nuevo')
    self.destroy()
    self.master.deiconify()

app=Aplicacion()
app.mainloop()