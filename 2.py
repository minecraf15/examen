import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import re
from fpdf import FPDF


def conectar_db():
    conexion = sqlite3.connect("conta.db")
    return conexion

def crear_tabla():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("CREATE TABLE IF NO EXISTS libro (id INTEGER PRIMARY KEY, tipo TEXT, cuenta TEXT, debe INTEGER, haber INTEGER)")
    conexion.commit()
    conexion.close()

def mostrar_datos():
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        consulta = "SELECT * FROM libro"
        cursor.execute(consulta)
        datos = cursor.fetchall()

        for item in tabla.get_children():
            tabla.delete(item)

        for dato in datos:
            tabla.insert("", "end", values=dato)

        cursor.close()
        conexion.close()

    except sqlite3.Error as error:
        mensaje_error("Error al cargar los datos: " + str(error))

def calcular_total():
    total_debe = 0
    total_haber = 0
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        consulta = "SELECT debe, haber FROM libro"
        cursor.execute(consulta)
        datos = cursor.fetchall()

        for dato in datos:
            debe_str = dato[0].replace("$", "").replace(",", "")
            haber_str = dato[1].replace("$", "").replace(",", "")
            debe = float(debe_str) if debe_str else 0
            haber = float(haber_str) if haber_str else 0
            total_debe += debe
            total_haber += haber

        total_debe_str = "${:,.2f}".format(total_debe)
        total_haber_str = "${:,.2f}".format(total_haber)

        for item in tabla_total.get_children():
            tabla_total.delete(item)

        tabla_total.insert("", "end", values=(total_debe_str, total_haber_str))

        cursor.close()
        conexion.close()

    except sqlite3.Error as error:
        mensaje_error("Error al calcular el total: " + str(error))

def guardar_datos():
    tipo = combo_tipo.get()
    cuenta = combo_cuenta.get()
    debe = entrada_debe.get()
    haber = entrada_haber.get()

    if sum(bool(valor) for valor in [tipo, cuenta, debe, haber]) < 3:
        mensaje_error("Debes completar al menos tres campos.")
        return

    if debe and haber:
        mensaje_error("Solo puedes guardar si una de las opciones de DEBE o HABER está completa.")
        return

    if not validar_caracteres():
        return
    try:
        debe = int(debe) if debe else 0
        haber = int(haber) if haber else 0

        debe_str = "${:,.2f}".format(debe)
        haber_str = "${:,.2f}".format(haber)

        conexion = conectar_db()
        cursor = conexion.cursor()
        consulta = "INSERT INTO libro (tipo, cuenta, debe, haber) VALUES (?, ?, ?, ?)"
        valores = (tipo, cuenta, debe_str, haber_str)
        cursor.execute(consulta, valores)
        conexion.commit()
        cursor.close()
        conexion.close()

        combo_tipo.set("")  
        combo_cuenta.set("")
        entrada_debe.delete(0, tk.END)
        entrada_haber.delete(0, tk.END)

    except sqlite3.Error as error:
        mensaje_error("Error al guardar los datos: " + str(error))



def validar_caracteres():
    debe = entrada_debe.get()
    haber = entrada_haber.get()

    if debe and not debe.isdigit():
        mensaje_error("El campo DEBE solo puede contener caracteres numéricos.")
        return False

    if haber and not haber.isdigit():
        mensaje_error("El campo HABER solo puede contener caracteres numéricos.")
        return False

    return True

def limpiar_campos():
    combo_tipo.set("")  
    combo_cuenta.set("")
    entrada_debe.delete(0, tk.END)
    entrada_haber.delete(0, tk.END)

def mensaje_error(mensaje):
    messagebox.showerror("Error", mensaje)

def filtrar_cuentas(*args):
    tipo_seleccionado = combo_tipo.get()

    if tipo_seleccionado == "Activos Circulantes":
        cuentas_disponibles = [
            "Caja",
            "Fondo fijo de caja chica",
            "Bancos",
            "Inversiones temporales",
            "Clientes",
            "Documentos por cobrar",
            "Deudores diversos",
            "Funcionarios y empleados",
            "IVA acreditable",
            "Almacén",
            "Anticipo a proveedores",
            "Papelería y útiles",
            "Propaganda y publicidad",
            "Prima de seguros y fianzas",
            "Rentas pagadas por anticipado",
            "Intereses pagados por anticipado"
        ]
    elif tipo_seleccionado == "Activos Fijos":
        cuentas_disponibles = [
            "Terrenos",
             "Edificios",
             "Depreciación acumulada de edificios",
             "Maquinaria",
             "Depreciación acumulada de maquinaria",
             "Mobiliario y equipo",
             "Depreciación acumulada de mobiliario y equipo",
             "Muebles y enseres",
             "Depreciación acumulada de muebles y enseres",
             "Equipo de transporte",
             "Depreciación acumulada de equipo de transporte",
             "Equipo de entrega y reparto",
             "Depreciación acumulada de equipo de entrega y reparto",
             "Equipo de cómputo",
             "Depreciación acumulada de equipo de cómputo"
        ]
    elif tipo_seleccionado == "Activos Intangibles":
        cuentas_disponibles = [
            "Derechos de autor",
            "Amortización acumulada de derechos de autor",
            "Patentes",
            "Amortización acumulada de patentes",
            "Marcas registradas",
            "Amortización acumulada de Marcas registradas",
            "Gastos de organización",
            "Amortización acumulada de gastos de organización",
            "Gastos de Instalación"
            "Amortizacion acomulada"
            "Papeleria y utiles"
            "Primas de seguros y fianzas"
            "Rentas pagadas por anticipo"
            "Intereses pagados por anticipo"
        ]
    elif tipo_seleccionado == "Pasivos a largo plazo":
        cuentas_disponibles = [
             "Documentos por pagar a largo plazo",
             "Acreedores bancarios",
             "Acreedores hipotecarios",
             "Rentas cobradas por anticipado",
             "Intereses cobrados por anticipo"
        ]
    elif tipo_seleccionado == "Pasivos a corto plazo":
        cuentas_disponibles = [
               "Proveedores",
               "Documentos por pagar",
               "Acreedores diversos",
               "Acreedores bancarios",
               "Anticipos de clientes",
               "Gastos acumulados",
               "Impuestos por pagar",
               "IVA trasladado",
               "Rentas cobradas por anticipado",
               "Intereses cobrados por anticipado"
        ]
    elif tipo_seleccionado == "Capital contable":
        cuentas_disponibles = [
             'Capital social',
             'Aportación para futuros aumentos de capital',
             'Prima de venta de acciones',
             'Capital donado'
        ]
    elif tipo_seleccionado == "Capital ganado":
        cuentas_disponibles = [
                "Utilidad del ejercicio",
                "Pérdida del ejercicio",
                "Utilidades retenidas",
                "Pérdidas acumuladas",
                "Reserva legal",
                "Dividendos"
        ]
    elif tipo_seleccionado == "Cuentas acredoras":
        cuentas_disponibles = [
            "Ventas",
            "Productos financieros",
            "Otros productos"
        ]
    elif tipo_seleccionado == "Cuentas deudoras":
        cuentas_disponibles = [
              "Costo de ventas",
              "Gastos de ventas",
              "Gastos de administración",
              "Gastos financieros",
              "Otros gastos",
              "Pérdidas y ganancias (deudora o acreedora)"
        ]
    else:
        cuentas_disponibles = []

    combo_cuenta['values'] = cuentas_disponibles
    combo_cuenta.set("")  

    combo_tipo.bind("<<ComboboxSelected>>", filtrar_cuentas)


def eliminar_registro():
    id_eliminar = entrada_eliminar.get()

    if not id_eliminar.isdigit():
        mensaje_error("El ID debe ser un número entero.")
        return

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        consulta = "SELECT * FROM libro WHERE id = ?"
        cursor.execute(consulta, (id_eliminar,))
        registro = cursor.fetchone()

        if registro is None:
            mensaje_error("El ID no existe en la base de datos.")
        else:
            consulta_eliminar = "DELETE FROM libro WHERE id = ?"
            cursor.execute(consulta_eliminar, (id_eliminar,))
            conexion.commit()
            mostrar_datos()

        cursor.close()
        conexion.close()
        crear_tabla()


    except sqlite3.Error as error:
        mensaje_error("Error al eliminar el registro: " + str(error))

def generar_pdf():
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=5)

    pdf.cell(35, 10, "ID", 1)
    pdf.cell(35, 10, "TIPO", 1)
    pdf.cell(35, 10, "CUENTA", 1)
    pdf.cell(35, 10, "DEBE", 1)
    pdf.cell(35, 10, "HABER", 1)
    pdf.ln()

    for item in tabla.get_children():
        values = tabla.item(item)["values"]
        for value in values:
            pdf.cell(35, 10, str(value), 1)
        pdf.ln()

    pdf.ln()
    pdf.cell(50, 10, "Total Debe", 1)
    pdf.cell(50, 10, "Total Haber", 1)
    pdf.ln()

    for item in tabla_total.get_children():
        values = tabla_total.item(item)["values"]
        for value in values:
            pdf.cell(50, 10, str(value), 1)
        pdf.ln()

    filename = filedialog.asksaveasfilename(defaultextension=".pdf")
    if filename:
        pdf.output(filename, "F")

def validar_longitud(text):
    return len(text) <= 15


def borrar_tabla():
    respuesta = messagebox.askquestion("Borrar operación", "¿Estás seguro de borrar la operación?")
    if respuesta == "yes":
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM libro")
        conexion.commit()
        cursor.close()
        conexion.close()
        messagebox.showinfo("Borrado exitoso", "La tabla ha sido borrada correctamente.")
        mostrar_datos()
    else:
        messagebox.showinfo("Operación cancelada", "La tabla no ha sido borrada.")

        
def crear_tabla():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS libro (id INTEGER PRIMARY KEY, tipo TEXT, cuenta TEXT, debe INTEGER, haber INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS cuadro (id INTEGER PRIMARY KEY, tipo TEXT, cuenta TEXT, debe INTEGER, haber INTEGER)")
    conexion.commit()
    conexion.close()

def actualizar_datos():
    mostrar_datos()

ventana = tk.Tk()

imagen = Image.open("imagen.png") 
imagen = imagen.resize((1200, 700)) 
imagen_tk = ImageTk.PhotoImage(imagen)
etiqueta_imagen = tk.Label(ventana, image=imagen_tk)
etiqueta_imagen.place(x=0, y=0)

tabla = ttk.Treeview

tabla = ttk.Treeview(ventana, columns=("ID", "TIPO", "CUENTA", "DEBE", "HABER"), show="headings")
tabla.heading("ID", text="ID")
tabla.heading("TIPO", text="TIPO")
tabla.heading("CUENTA", text="CUENTA")
tabla.heading("DEBE", text="DEBE")
tabla.heading("HABER", text="HABER")

tabla.column("ID", width=100)
tabla.column("TIPO", width=100)
tabla.column("CUENTA", width=100)
tabla.column("DEBE", width=100)
tabla.column("HABER", width=100)

tabla.place(x=200,y=70)

tabla_total = ttk.Treeview(ventana, columns=("Total Debe","Total Haber"), show="headings")
tabla_total.place(x=500,y=320)

tabla_total.heading("Total Debe", text="Total Debe")
tabla_total.heading("Total Haber", text="Total Haber")

tabla_total.column("Total Debe", width=100)
tabla_total.column("Total Haber", width=100)
tabla_total["height"] = 3

etiqueta_tipo = tk.Label(ventana, text="TIPO", bg="pink")
etiqueta_tipo.grid(row=1, column=0, padx=30, pady=5, sticky="w")

combo_tipo = ttk.Combobox(ventana, values=[
    "Activos Circulantes",
    "Activos Fijos",
    "Activos Intangibles",
    "Pasivos a largo plazo",
    "Pasivos a corto plazo",
    "Capital contable",
    "Capital ganado",
    "Cuentas acredoras",
    "Cuentas deudoras"
])
combo_tipo.grid(row=2, column=0, padx=30, pady=5, sticky="w")
combo_tipo.config(state="readonly")
combo_tipo.bind("<<ComboboxSelected>>", filtrar_cuentas)

etiqueta_cuenta = tk.Label(ventana, text="CUENTA",bg="pink")
etiqueta_cuenta.grid(row=3, column=0, padx=30, pady=5, sticky="w")

combo_cuenta = ttk.Combobox(ventana, values=[""])
combo_cuenta.grid(row=4, column=0, padx=30, pady=5, sticky="w")
combo_cuenta.config(state="readonly")

etiqueta_eliminar = tk.Label(ventana, text="INGRESE EL ID A ELIMINAR", bg="pink", anchor="e")
etiqueta_eliminar.place(x=220, y=320)

entrada_eliminar = tk.Entry(ventana)
entrada_eliminar.place(x=227, y=350)

etiqueta_haber = tk.Label(ventana, text="HABER", bg="pink")
etiqueta_haber.grid(row=6, column=0, padx=30, pady=5, sticky="w")

entrada_haber = tk.Entry(ventana, validate="key", validatecommand=(ventana.register(validar_longitud), '%P'))
entrada_haber.grid(row=7, column=0, padx=30, pady=5, sticky="w")

etiqueta_debe = tk.Label(ventana, text="DEBE", bg="pink")
etiqueta_debe.grid(row=8, column=0, padx=30, pady=5, sticky="w")

entrada_debe = tk.Entry(ventana, validate="key", validatecommand=(ventana.register(validar_longitud), '%P'))
entrada_debe.grid(row=9, column=0, padx=30, pady=5, sticky="w")

boton_monto_total = tk.Button(ventana, text="MONTO TOTAL", bg="lightpink", command=calcular_total)
boton_monto_total.place(x=600,y=415)
boton_monto_total.config(font=("Helvetica", 9, "bold"))
boton_monto_total.config(foreground="black", activebackground="skyblue")

boton_guardar = tk.Button(ventana, text="GUARDAR", bg="lightpink", command=guardar_datos)
boton_guardar.grid(row=10, column=0, padx=20, pady=5, sticky="w")
boton_guardar.config(font=("Helvetica", 9, "bold"))
boton_guardar.config(foreground="black", activebackground="skyblue")

boton_mostrar = tk.Button(ventana, text="MOSTRAR DATOS", bg="lightpink", command=mostrar_datos)
boton_mostrar.grid(row=11, column=0, padx=19, pady=(0, 5), sticky="w")
boton_mostrar.config(font=("Helvetica", 9, "bold"))
boton_mostrar.config(foreground="black", activebackground="skyblue")

boton_limpiar = tk.Button(ventana, text="LIMPIAR", bg="lightpink", command=limpiar_campos, anchor="w")
boton_limpiar.grid(row=10, column=0, padx=95, pady=5, sticky="w")
boton_limpiar.config(font=("Helvetica", 9, "bold"))
boton_limpiar.config(foreground="black", activebackground="skyblue")

boton_actualizar = tk.Button(ventana, text="ACTUALIZAR", bg="lightpink", command=actualizar_datos)
boton_actualizar.grid(row=12, column=0, padx=19, pady=(0, 5), sticky="w")
boton_actualizar.config(font=("Helvetica", 9, "bold"))
boton_actualizar.config(foreground="black", activebackground="skyblue")

boton_eliminar = tk.Button(ventana, text="ELIMINAR", bg="lightpink", command=eliminar_registro)
boton_eliminar.place(x=250, y=380)
boton_eliminar.config(font=("Helvetica", 9, "bold"))
boton_eliminar.config(foreground="black", activebackground="skyblue")

boton_descargar = tk.Button(ventana, text="DESCARGAR PDF", bg="lightpink", command=generar_pdf)
boton_descargar.place(x=470,y=20)
boton_descargar.config(font=("Helvetica", 9, "bold"))
boton_descargar.config(foreground="black", activebackground="skyblue")

boton_actualizar = tk.Button(ventana, text="TERMINAR", bg="lightpink", command=borrar_tabla)
boton_actualizar.place(x=630,y=20)
boton_actualizar.config(font=("Helvetica", 9, "bold"))
boton_actualizar.config(foreground="black", activebackground="skyblue")

ventana.title("BIENVENIDO AL SISTEMA DE ASIENTOS CONTABLES")
ventana.geometry("850x500")
ventana.resizable(False,False)

crear_tabla()
ventana.mainloop() 