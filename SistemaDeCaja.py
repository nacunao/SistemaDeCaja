import sys

# Librerías Interfaz Gráfica Tkinter
from tkinter import *
from tkinter import ttk
from tkcalendar import dateentry 
from datetime import *

# Librería conexión base de datos por medio de mysql
import mysql.connector

# Librerías edición docx
from pathlib import Path
from docxtpl import DocxTemplate
import os


# Librerías impresión
from win32 import win32print
from win32 import win32api

# LISTAS ASUNTO
lista_asunto_ingreso=[
    'ARRIENDO',
    'ARRIENDO CONFITERIA EL FORTÍN',
    'ARRIENDO ACHAVAR',
    'ARRIENDO RESTAURANT LA VERTIENTE',
    'ARRIENDO RESTAURANT KOPPA',
    'ARRIENDO RESTAURANT CLAUDIA',
    'ARRIENDO SEGUT',
    'ARRIENDO CAFETERIA',
    'ARRIENDO FIN DE SEMANA',
    'PASE JUGADOR',
    'PRÉSTAMO JUGADOR',
    'BORDERÓ',
    'APORTE',
    'PUBLICIDAD',
    'FONDOS CONCURSABLES',
    'APORTE PARTICULAR',
    'OTRO']
lista_asunto_egreso=[
    'REMUNERACIONES',
    'HONORARIOS',
    'CONTRIBUCIONES',
    'CELULAR',
    'CAJA CHICA',
    'MANTENCIÓN GENERAL',
    'MANTENCIÓN ELECTRÓNICA',
    'ARBITROS',
    'CRONOMETRISTA',
    'DEUDA CONVENIO',
    'GASTOS COPA PANCHO',
    'TRABAJO EXTRA',
    'TRANSPORTE',
    'COMUNICACIONES',
    'AGUINALDO',
    'VARIOS',
    'OTRO'
]

# LISTAS RECIBIDO DE/ENVIADO A
lista_recibido_de=[
    'LIN DIAZ'
    'SAMUEL BERNAL',
    'ERIKA BERNAL',
    'MUNICIPALIDAD',
    'PUERTO VALPARAISO',
    'PARTICULAR',
    'OTRO']
lista_enviado_a=[
    'PREVIRED'
    'TESORERÍA GENERAL DE LA REPÚBLICA',
    'CHILQUINTA',
    'GASVALPO',
    'ESVAL',
    'OTRO'
]

#------------ SECCIÓN FUNCIÓN MONTO EN PALABRAS -------------------------------
MAX_NUMERO = 999999999999

UNIDADES = (
    'CERO',
    'UNO',
    'DOS',
    'TRES',
    'CUATRO',
    'CINCO',
    'SEIS',
    'SIETE',
    'OCHO',
    'NUEVE'
)

DECENAS = (
    'DIEZ',
    'ONCE',
    'DOCE',
    'TRECE',
    'CATORCE',
    'QUINCE',
    'DIECISEIS',
    'DIECISIETE',
    'DIECIOCHO',
    'DIECINUEVE'
)

DIEZ_DIEZ = (
    'CERO',
    'DIEZ',
    'VEINTE',
    'TREINTA',
    'CUARENTA',
    'CINCUENTA',
    'SESENTA',
    'SETENTA',
    'OCHENTA',
    'NOVENTA'
)

CIENTOS = (
    '_',
    'CIENTO',
    'DOSCIENTOS',
    'TRESCIENTOS',
    'CUATROSCIENTOS',
    'QUINIENTOS',
    'SEISCIENTOS',
    'SETECIENTOS',
    'OCHOCIENTOS',
    'NOVECIENTOS'
)

class Formato:
    def __init__(self) -> None:
        pass

    def numero_a_moneda_sunat(self, numero):
        numero_entero = int(numero)
        letras = numero_a_letras(numero_entero)
        letras = letras.replace('UNO', 'UN')
        letras = f"{letras}"
        return letras

    
def numero_a_letras(numero):
    numero_entero = int(numero)
    if numero_entero > MAX_NUMERO:
        raise OverflowError('Número demasiado alto')
    if numero_entero < 0:
        negativo_letras = numero_a_letras(abs(numero))
        return f"MENOS {negativo_letras}"
    if numero_entero <= 99:
        resultado = leer_decenas(numero_entero)
    elif numero_entero <= 999:
        resultado = leer_centenas(numero_entero)
    elif numero_entero <= 999999:
        resultado = leer_miles(numero_entero)
    elif numero_entero <= 999999999:
        resultado = leer_millones(numero_entero)
    else:
        resultado = leer_millardos(numero_entero)
    resultado = resultado.replace('UNO MIL', 'UN MIL')
    resultado = resultado.strip()
    resultado = resultado.replace(' _ ', ' ')
    resultado = resultado.replace('  ', ' ')
    return resultado


def numero_a_moneda(numero):
    numero_entero = int(numero)
    letras = numero_a_letras(numero_entero)
    letras = letras.replace('UNO', 'UN')
    letras = f"{letras}"
    return letras


def leer_decenas(numero):
    if numero < 10:
        return UNIDADES[numero]
    decena, unidad = divmod(numero, 10)
    if numero <= 19:
        resultado = DECENAS[unidad]
    elif numero <= 29:
        resultado = f"VEINTI{UNIDADES[unidad]}"
    else:
        resultado = DIEZ_DIEZ[decena]
        if unidad > 0:
            resultado = f"{resultado} Y {UNIDADES[unidad]}"
    return resultado


def leer_centenas(numero):
    centena, decena = divmod(numero, 100)
    if numero == 0:
        resultado = 'CIEN'
    else:
        resultado = CIENTOS[centena]
        if decena > 0:
            decena_letras = leer_decenas(decena)
            resultado = f"{resultado} {decena_letras}"
    return resultado


def leer_miles(numero):
    millar, centena = divmod(numero, 1000)
    resultado = ''
    if millar == 1:
        resultado = ''
    if (millar >= 2) and (millar <= 9):
        resultado = UNIDADES[millar]
    elif (millar >= 10) and (millar <= 99):
        resultado = leer_decenas(millar)
    elif (millar >= 100) and (millar <= 999):
        resultado = leer_centenas(millar)
    resultado = f"{resultado} MIL"
    if centena > 0:
        centena_letras = leer_centenas(centena)
        resultado = f"{resultado} {centena_letras}"
    return resultado.strip()


def leer_millones(numero):
    millon, millar = divmod(numero, 1000000)
    resultado = ''
    if millon == 1:
        resultado = ' UN MILLON '
    if (millon >= 2) and (millon <= 9):
        resultado = UNIDADES[millon]
    elif (millon >= 10) and (millon <= 99):
        resultado = leer_decenas(millon)
    elif (millon >= 100) and (millon <= 999):
        resultado = leer_centenas(millon)
    if millon > 1:
        resultado = f"{resultado} MILLONES"
    if (millar > 0) and (millar <= 999):
        centena_letras = leer_centenas(millar)
        resultado = f"{resultado} {centena_letras}"
    elif (millar >= 1000) and (millar <= 999999):
        miles_letras = leer_miles(millar)
        resultado = f"{resultado} {miles_letras}"
    return resultado


def leer_millardos(numero):
    millardo, millon = divmod(numero, 1000000)
    miles_letras = leer_miles(millardo)
    millones_letras = leer_millones(millon)
    return f"{miles_letras} MILLONES {millones_letras}"


#---------------------------- Conexión a la base de datos remota ----------------------
def conectar_BaseDeDatos(opcion):
    conexion_bdd = mysql.connector.connect(
        user='hpn9tpk1dry0lmzu7377', # Usuario
        password='pscale_pw_z8FWTgp8gcRZJUEmtlO1GTY2mep54VHI46hlq7lxyOm', # Contraseña
        host='us-east.connect.psdb.cloud', # Host
        database='administracion-ingresos-egresos') # Nombre de la base de datos
    
    # Importar la base de datos
    if opcion==1:
        mycursor = conexion_bdd.cursor()
        mycursor.execute("SELECT * FROM Transaccion") # Sentencia MYSQL: Se seleccionan de todos los elementos de la base de datos
        fila = mycursor.fetchall()

        # Se insertan en la tabla todos los elementos de la base de datos
        for dato in fila:
            n=str(dato[0])
            if dato[6]!=0:
                tabla.insert('', 'end', values=(n[len(n)-5]+'-'+n[-4:], dato[1], dato[2], dato[3], dato[4].strftime("%d-%m-%Y"), dato[5], dato[6], dato[7], dato[8]))
            else: tabla.insert('', 'end', values=(n[len(n)-5]+'-'+n[-4:], dato[1], dato[2], dato[3], dato[4].strftime("%d-%m-%Y"), dato[5], "--------", dato[7], dato[8]))
    
    # Agregar elemento a la base de datos
    elif opcion==2:
        mycursor=conexion_bdd.cursor()
        mycursor.execute("SELECT COUNT(*) FROM Transaccion WHERE CAST(numero AS CHAR(10)) LIKE '%"+str(fecha.year)+"' AND `tipo` LIKE '"+str(tipo)+"'") # Sentencia MYSQL: Se cuentan todos los ingresos o egresos de un mismo año
        fila = mycursor.fetchall()
        global numero
        numero = int(str(int(fila[0][0])+1)+str(fecha.year))

        sql = "INSERT INTO Transaccion (numero, tipo, asunto, persona, fecha, medio, nCheque, monto, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" # Sentenica MYSQL: Se inserta la fila nueva con sus datos
        valores = (numero, tipo, asunto, persona, date.isoformat(fecha), medio, ncheque, monto, descripcion)


        mycursor = conexion_bdd.cursor()
        mycursor.execute(sql, valores)
        conexion_bdd.commit()

        # El elemento nuevo se inserta en la tabla para mantener ésta actualizada
        n=str(numero)
        if ncheque!=0:
            tabla.insert('', 'end', values=(n[len(n)-5]+'-'+n[-4:], tipo, asunto, persona, fecha.strftime("%d-%m-%Y"), medio, ncheque, monto, descripcion))
        else: tabla.insert('', 'end', values=(n[len(n)-5]+'-'+n[-4:], tipo, asunto, persona, fecha.strftime("%d-%m-%Y"), medio, "--------", monto, descripcion))

    # Buscar en la base de datos por persona (Recibido de:/Enviado a:)
    elif opcion==3:
        # Se hace la busqueda sí se ingreso una cadena de largo mayor a 2 carácteres 
        if len(busqueda_var.get())>2:
            tabla.delete(*tabla.get_children()) # Se elimina el contenido de la tabla actual
            mycursor = conexion_bdd.cursor()
            mycursor.execute("SELECT * FROM Transaccion WHERE `persona` LIKE '%"+busqueda_var.get()+"%'") # Sentencia MYSQL: Se seleccionan los elementos cuya persona contenga carácteres de la ingresada
            fila = mycursor.fetchall()
            # Se insertan en la tabla los datos de la búsqueda
            for dato in fila:
                n=str(dato[0])
                if dato[6]!=0:
                    tabla.insert('', 'end', values=(n[len(n)-5]+'-'+n[-4:], dato[1], dato[2], dato[3], dato[4].strftime("%d-%m-%Y"), dato[5], dato[6], dato[7], dato[8]))
                else: tabla.insert('', 'end', values=(n[len(n)-5]+'-'+n[-4:], dato[1], dato[2], dato[3], dato[4].strftime("%d-%m-%Y"), dato[5], "--------", dato[7], dato[8]))
    
    # Limpiar busqueda de la base de datos
    elif opcion==4:
        tabla.delete(*tabla.get_children()) # Se elimina el contenido de la tabla actual
        tabla.heading('4', text="Recibido de/Enviado a", anchor=W)
        mycursor = conexion_bdd.cursor()
        mycursor.execute("SELECT * FROM Transaccion") # Sentencia MYSQL: Se seleccionan de todos los elementos de la base de datos
        fila = mycursor.fetchall()

        # Se insertan en la tabla todos los elementos de la base de datos
        for dato in fila:
            n=str(dato[0])
            if dato[6]!=0:
                tabla.insert('', 'end', values=(n[len(n)-5]+'-'+n[-4:], dato[1], dato[2], dato[3], dato[4].strftime("%d-%m-%Y"), dato[5], dato[6], dato[7], dato[8]))
            else: tabla.insert('', 'end', values=(n[len(n)-5]+'-'+n[-4:], dato[1], dato[2], dato[3], dato[4].strftime("%d-%m-%Y"), dato[5], "--------", dato[7], dato[8]))

    # Filtrar Tabla
    else:
        tabla.delete(*tabla.get_children()) # Se elimina el contenido de la tabla actual
        mycursor = conexion_bdd.cursor()
        if filtroTipo_var.get()!='Todos':
            mycursor.execute("SELECT * FROM Transaccion WHERE `tipo` LIKE '"+filtroTipo_var.get()+"'") # Sentencia MYSQL: Se seleccionan los elementos del tipo seleccionado
            if filtroTipo_var.get()=='Ingreso':
                tabla.heading('4', text="Recibido de", anchor=W)
            else: tabla.heading('4', text="Enviado a", anchor=W)
        else:
            mycursor.execute("SELECT * FROM Transaccion")
            tabla.heading('4', text="Recibido de/Enviado a", anchor=W)
        fila = mycursor.fetchall()
        
        # Se insertan en la tabla los datos seleccionados
        for dato in fila:
            n=str(dato[0])
            if dato[6]!=0:
                tabla.insert('', 'end', values=(n[len(n)-5]+'-'+n[-4:], dato[1], dato[2], dato[3], dato[4].strftime("%d-%m-%Y"), dato[5], dato[6], dato[7], dato[8]))
            else: tabla.insert('', 'end', values=(n[len(n)-5]+'-'+n[-4:], dato[1], dato[2], dato[3], dato[4].strftime("%d-%m-%Y"), dato[5], "--------", dato[7], dato[8]))

            
    conexion_bdd.close() # Se cierra la conexión a la base de datos remota



#====================================VENTANA PRINCIPAL=========================================
class Aplicacion(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Sistema de Caja")
        width = 1200 # ancho de la ventana
        height = 675 # alto de la ventana
        x = 20
        y = 20
        self.master.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        self.master.resizable(width=False, height=False)
        self.master.configure(bg='#FFFFFF')
        self.master.iconbitmap(sys.executable)




        # Frames: Contenedores dentro de la ventana que contienen los elementos
        contenedor1=LabelFrame(self.master, text="Buscador Persona", bg='#8297BC', fg='#FFFFFF')
        contenedor1.place(x=40, y=10, width=575, height=75)
        contenedor2=LabelFrame(self.master, text="Operaciones", bg='#E64611', fg='#FFFFFF')
        contenedor2.place(x=40, y=580, width=375, height=75)
        contenedorTabla=Frame(self.master, bg='#EDB712')
        contenedorTabla.place(x=40, y=120, width=1120, height=420)
        contenedorFiltroTipo=LabelFrame(self.master, text="Filtrar por tipo", bg='#C5A97B', fg='#FFFFFF')
        contenedorFiltroTipo.place(x=630, y=10, width=220, height=75)
        
        # Tabla
        global tabla
        global barra1
        global barra2
        tabla = ttk.Treeview(contenedorTabla, selectmode='extended')
        tabla.place(x=10, y=10, width=1080, height=380)
        tabla['columns']=("1", "2", "3", "4", "5", "6", "7", "8", "9")
        tabla['show']='headings'
        barra1=Scrollbar(contenedorTabla, orient=HORIZONTAL, command=tabla.xview)
        barra1.place(x=10, y=395, width=1080)
        barra2=Scrollbar(contenedorTabla, orient=VERTICAL, command=tabla.yview)
        barra2.place(x=1095, y=10, height=380)
        
        tabla.configure(xscrollcommand=barra1.set, yscrollcommand=barra2.set)

        estilo_tabla=ttk.Style()
        estilo_tabla.configure('Treeview.Heading', font=('Helvetica', 11), rowheigth=40)
        estilo_tabla.configure('Treeview', font=('Helvetica', 11), rowheigth=40)
        estilo_tabla.map('Treeview', background=[('selected', 'silver')])


        tabla.heading('1', text="Número", anchor=W)
        tabla.heading('2', text="Tipo", anchor=W)
        tabla.heading('3', text="Asunto", anchor=W)
        tabla.heading('4', text="Recibido de/Enviado a", anchor=W)
        tabla.heading('5', text="Fecha", anchor=W)
        tabla.heading('6', text="Medio", anchor=W)
        tabla.heading('7', text="Número de Cheque", anchor=W)
        tabla.heading('8', text="Monto", anchor=W)
        tabla.heading('9', text="Por concepto de", anchor=W)
        
        tabla.column('1', stretch=NO, minwidth=80, width=80)
        tabla.column('2', stretch=NO, minwidth=100, width=100)
        tabla.column('3', stretch=NO, minwidth=300, width=300)
        tabla.column('4', stretch=NO, minwidth=300, width=300)
        tabla.column('5', stretch=NO, minwidth=100, width=100)
        tabla.column('6', stretch=NO, minwidth=100, width=100)
        tabla.column('7', stretch=NO, minwidth=150, width=150)
        tabla.column('8', stretch=NO, minwidth=100, width=100)
        tabla.column('9', stretch=NO, minwidth=500, width=500)

        # Conexión con la base de datos (importación de datos)
        conectar_BaseDeDatos(1)

        global busqueda_var
        busqueda_var=StringVar()

        def habilitar_boton(evento):
            if len(entrada1.get())>0:
                boton1['state']=NORMAL
            else: boton1['state']=DISABLED
        # Entradas
        global entrada1
        entrada1=Entry(contenedor1, textvariable=busqueda_var)
        entrada1.place(x=20, y=10, width=350, height=32)
        self.master.bind('<KeyRelease>', habilitar_boton)
        
        
        global filtroTipo_var
        filtroTipo_var=StringVar(value='Todos')

        # Combobox
        combo_tipo=ttk.Combobox(contenedorFiltroTipo, values=['Todos', 'Ingreso', 'Egreso'], textvariable=filtroTipo_var, font=("Helvetica", 12), state='readonly')
        combo_tipo.place(x=10, y=10, width=200)
        combo_tipo.bind('<<ComboboxSelected>>', self.filtrar_tabla)


        # Botones
        boton1=Button(contenedor1, text="Buscar", command=self.buscar_persona, font=("Helvetica", 12), bg='#FFFFFF', borderwidth=0)
        boton1.place(x=400, y=10)
        boton1['state']=DISABLED
        boton2=Button(contenedor1, text="Limpiar", command=self.limpiar_tabla, font=("Helvetica", 12), bg='#FFFFFF', borderwidth=0)
        boton2.place(x=475, y=10)
        boton3=Button(contenedor2, text="Agregar Ingreso", command=self.abrir_ventanaSecundaria1, font=("Helvetica", 12), bg='#FFFFFF', borderwidth=0)
        boton3.place(x=20, y=10)
        boton4=Button(contenedor2, text="Agregar Egreso", command=self.abrir_ventanaSecundaria2, font=("Helvetica", 12), bg='#FFFFFF', borderwidth=0)
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
        entrada1.delete(0, 'end')
        conectar_BaseDeDatos(4)

    def filtrar_tabla(self, evento):
        conectar_BaseDeDatos(5)

    def actualizar_tabla(self):
        conectar_BaseDeDatos(4)



#=================================VENTANA SECUNDARIA AGREGAR INGRESO===========================
class VentanaSecundariaAgregarIngreso(Frame):
    def __init__(self):
        self.nuevo=Frame.__init__(self)
        self.nuevo=Toplevel(self)
        self.nuevo.protocol("WM_DELETE_WINDOW", disable_event)
        self.nuevo.configure(bg='#FFFFFF')
        self.nuevo.title("Agregar Ingreso")
        width=760
        height=610
        x = 20
        y = 20
        self.nuevo.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        self.nuevo.resizable(width=False, height=False)
        self.nuevo.iconbitmap(sys.executable)
        
        inicializar_variables(self)
        inicializar_radioBotones(self)
        inicializar_componentes(self, "Ingreso", "Inicio")


#===============================VENTANA SECUNDARIA AGREGAR EGRESO==============================
class VentanaSecundariaAgregarEgreso(Frame):
    def __init__(self):
        self.nuevo=Frame.__init__(self)
        self.nuevo=Toplevel(self)
        self.nuevo.protocol("WM_DELETE_WINDOW", disable_event)
        self.nuevo.configure(bg='#FFFFFF')
        self.nuevo.title("Agregar Egreso")
        width=760
        height=610
        x = 20
        y = 20
        self.nuevo.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        self.nuevo.resizable(width=False, height=False)
        self.nuevo.iconbitmap(sys.executable)
        
        inicializar_variables(self)
        inicializar_radioBotones(self)
        inicializar_componentes(self, "Egreso", "Inicio")
        


#================== Funciones de inicialización componentes ventanas secundarias agregar ingreso y agregar egreso ==================
def inicializar_variables(self):
    self.asunto_var=StringVar()
    self.asuntoOtro_var=StringVar()
    self.persona_var=StringVar()
    self.personaOtra_var=StringVar() 
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
            if self.entrada1.get()=='OTRO' and self.entrada2.get()=='OTRO':
                if len(self.entrada1_adicional.get())>0 and len(self.entrada2_adicional.get())>0 and len(self.entrada4.get())>0 and len(self.entrada5.get())>0 and len(self.entrada6.get("1.0", "end-1c")):
                    self.boton2['state']=NORMAL
                else: self.boton2['state']=DISABLED
            elif self.entrada1.get()=='OTRO' and self.entrada2.get()!='OTRO':
                if len(self.entrada1_adicional.get())>0 and len(self.entrada2.get())>0 and len(self.entrada4.get())>0 and len(self.entrada5.get())>0 and len(self.entrada6.get("1.0", "end-1c")):
                    self.boton2['state']=NORMAL
                else: self.boton2['state']=DISABLED
            elif self.entrada1.get()!='OTRO' and self.entrada2.get()=='OTRO':
                if len(self.entrada1.get())>0 and len(self.entrada2_adicional.get())>0 and len(self.entrada4.get())>0 and len(self.entrada5.get())>0 and len(self.entrada6.get("1.0", "end-1c")):
                    self.boton2['state']=NORMAL
                else: self.boton2['state']=DISABLED
            else:
                if len(self.entrada1.get())>0 and len(self.entrada2.get())>0 and len(self.entrada4.get())>0 and len(self.entrada5.get())>0 and len(self.entrada6.get("1.0", "end-1c")):
                    self.boton2['state']=NORMAL
                else: self.boton2['state']=DISABLED
        else:
            if self.entrada1.get()=='OTRO' and self.entrada2.get()=='OTRO':
                if len(self.entrada1_adicional.get())>0 and len(self.entrada2_adicional.get())>0 and len(self.entrada5.get())>0 and len(self.entrada6.get("1.0", "end-1c")):
                    self.boton2['state']=NORMAL
                else: self.boton2['state']=DISABLED
            elif self.entrada1.get()=='OTRO' and self.entrada2.get()!='OTRO':
                if len(self.entrada1_adicional.get())>0 and len(self.entrada2.get())>0 and len(self.entrada5.get())>0 and len(self.entrada6.get("1.0", "end-1c")):
                    self.boton2['state']=NORMAL
                else: self.boton2['state']=DISABLED
            elif self.entrada1.get()!='OTRO' and self.entrada2.get()=='OTRO':
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
        def comboboxclick1(evento):
            if self.asunto_var.get() !='OTRO':
                self.entrada1_adicional.place_forget()
            else:
                self.entrada1_adicional.place(x=330, y=5, width=310, height=32)
        self.entrada1=ttk.Combobox(self.contenedor1, textvariable=self.asunto_var, font=("Helvetica", 13), state='readonly')
        if tipo=="Ingreso":
            self.entrada1['values']=lista_asunto_ingreso
        else:
            self.entrada1['values']=lista_asunto_egreso
        self.entrada1.bind("<<ComboboxSelected>>", comboboxclick1)
        self.entrada1.place(x=10, y=5, width=310, height=32)
        self.entrada1_adicional=Entry(self.contenedor1, textvariable=self.asuntoOtro_var, font=("Helvetica", 13))

        def comboboxclick2(evento):
            if self.persona_var.get() !='OTRO':
                self.entrada2_adicional.place_forget()
            else:
                self.entrada2_adicional.place(x=330, y=5, width=310, height=32)

        self.entrada2=ttk.Combobox(self.contenedor2, textvariable=self.persona_var, font=("Helvetica", 13), state='readonly')
        if tipo=="Ingreso":
            self.entrada2['values']=lista_recibido_de
        else:
            self.entrada2['values']=lista_enviado_a
        self.entrada2.bind("<<ComboboxSelected>>", comboboxclick2)
        self.entrada2.place(x=10, y=5, width=310, height=32)
        self.entrada2_adicional=Entry(self.contenedor2, textvariable=self.personaOtra_var, font=("Helvetica", 13))

        self.entrada3=dateentry.DateEntry(self.contenedor3, state='readonly', locale='es_CL', date_pattern='dd-mm-yyyy', width=50)
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
        self.checkBox=Checkbutton(self.nuevo, text="¿Desea imprimir los datos del "+tipo+"?", variable=self.imprimir, onvalue=TRUE, offvalue=FALSE, font=("Helvetica", 12))
        self.checkBox.configure(bg='#FFFFFF')
        self.checkBox.place(x=40, y=570)

        # Botones
        self.boton1=Button(self.nuevo, text="Regresar", command=lambda:cerrar_ventanaSecundaria(self), font=("Helvetica", 13), borderwidth=0)
        self.boton1.configure(bg='#FFD1A5')
        self.boton1.place(x=500, y=570)

        self.boton2=Button(self.nuevo, text="Agregar", command=lambda:crearTransaccion(self, tipo), font=("Helvetica", 13), borderwidth=0)
        self.boton2.configure(bg='#FFD1A5')
        self.boton2.place(x=630, y=570)
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
    global tipo
    global asunto
    global persona
    global fecha
    global medio
    global ncheque
    global monto
    global descripcion
    asunto=self.entrada1.get()
    if asunto=='OTRO':
        asunto=self.entrada1_adicional.get()
    persona=self.entrada2.get()
    if persona=='OTRO':
        persona=self.entrada2_adicional.get()
    fecha=self.entrada3.get_date()
    medio=self.medio_var.get()
    if medio=="Cheque":
        ncheque=int(self.entrada4.get())
    else: ncheque=0
    monto=int(self.entrada5.get())
    descripcion=self.entrada6.get("1.0", "end-1c")
    tipo=t
    
    conectar_BaseDeDatos(2) # Conexión a la base de datos (agregar elemento)
    if self.imprimir.get()==TRUE:
        crear_documento()
        imprimir_documento()
    cerrar_ventanaSecundaria(self)

# Función que busca la ruta del archivo 
def findfile(name, path):
    for dirpath, dirname, filename in os.walk(path):
        if name in filename:
            return os.path.join(dirpath, name)
    
# Función que crea el documento con los datos el elemento nuevo a partir de una plantilla
def crear_documento():
    if tipo=='Ingreso':
        filepath = findfile("plantilla_documento_ingreso.docx", "\\")
        plantilla_documento = Path(filepath).parent / "plantilla_documento_ingreso.docx"
    else:
        filepath = findfile("plantilla_documento_egreso.docx", "\\")
        plantilla_documento = Path(filepath).parent / "plantilla_documento_egreso.docx"
    documento = DocxTemplate(plantilla_documento)

    f=Formato()
    monto_en_palabras=f.numero_a_moneda_sunat(monto)

    n=str(numero)


    if medio=='Cheque':
        context = {
            "NUMERO": n[len(n)-5]+'-'+n[-4:],
            "ASUNTO": asunto,
            "PERSONA": persona,
            "FECHA": fecha.strftime("%d-%m-%Y"),
            "CHEQUE": ncheque,
            "E": "",
            "T": "",
            "MONTO": '{:,}'.format(monto).replace(',','.'),
            "MONTO_PALABRAS": monto_en_palabras,
            "DESCRIPCION": descripcion,
        }
    elif medio=='Efectivo':
        context = {
            "NUMERO": n[len(n)-5]+'-'+n[-4:],
            "ASUNTO": asunto,
            "PERSONA": persona,
            "FECHA": fecha.strftime("%d-%m-%Y"),
            "CHEQUE": "",
            "E": "X",
            "T": "",
            "MONTO": '{:,}'.format(monto).replace(',','.'),
            "MONTO_PALABRAS": monto_en_palabras,
            "DESCRIPCION": descripcion,
        }
    else:
        context = {
            "NUMERO": n[len(n)-5]+'-'+n[-4:],
            "ASUNTO": asunto,
            "PERSONA": persona,
            "FECHA": fecha.strftime("%d-%m-%Y"),
            "CHEQUE": "",
            "E": "",
            "T": "X",
            "MONTO": '{:,}'.format(monto).replace(',','.'),
            "MONTO_PALABRAS": monto_en_palabras,
            "DESCRIPCION": descripcion,
        }

    documento.render(context)
    documento.save(Path(filepath).parent / f"{numero}_{tipo}.docx")
    global rod
    rod =os.path.dirname(os.path.abspath(filepath))

# Función que Imprime el documento en la impresora predeterminada
def imprimir_documento():
    name = win32print.GetDefaultPrinter()
    printdefaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
    handle = win32print.OpenPrinter(name, printdefaults)
    level = 2
    attributes = win32print.GetPrinter(handle, level)
    attributes['pDevMode'].Duplex = 3 
    win32print.SetPrinter(handle, level, attributes, 0)
    win32print.GetPrinter(handle, level)['pDevMode'].Duplex
    
    win32api.ShellExecute(0, "print", rod+"\\"+str(numero)+"_"+tipo+".docx", None,  ".",  0)
    win32print.ClosePrinter(handle)
    

def disable_event():
   pass

def cerrar_ventanaSecundaria(self):
    self.destroy()
    self.master.deiconify()

app=Aplicacion()
app.mainloop()





