import tkinter as tk
from tkinter import ttk
from collections import deque
from datetime import datetime

import serial
from serial.tools import list_ports

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ventana = tk.Tk()
ventana.title("Smart Greenhouse")
ventana.geometry("1050x750")
ventana.configure(bg="#10231e")

arduino = None
buffer = bytearray()

temperaturas = deque(maxlen=30)
humedades = deque(maxlen=30)

tk.Label(
    ventana,
    text="SMART GREENHOUSE",
    font=("Arial", 28, "bold"),
    bg="#10231e",
    fg="#80d9a0"
).pack(pady=15)

tk.Label(
    ventana,
    text="Sistema inteligente de monitoreo ambiental",
    bg="#10231e",
    fg="white",
    font=("Arial", 12)
).pack()

barra = tk.Frame(ventana, bg="#10231e")
barra.pack(pady=15)

puertos = ttk.Combobox(barra, width=15, state="readonly")
puertos.pack(side="left", padx=5)

estado = tk.StringVar(value="Desconectado")


def actualizar_puertos():
    disponibles = [p.device for p in list_ports.comports()]
    puertos["values"] = disponibles
    if disponibles:
        puertos.current(0)


def conectar():
    global arduino

    if arduino and arduino.is_open:
        arduino.close()
        arduino = None
        estado.set("Desconectado")
        return

    try:
        buffer.clear()
        arduino = serial.Serial(
            puertos.get(), 9600, timeout=0
        )
        estado.set("Conectado")
    except Exception:
        estado.set("Error de conexion")


ttk.Button(
    barra, text="Buscar puertos",
    command=actualizar_puertos
).pack(side="left", padx=5)

ttk.Button(
    barra, text="Conectar / Desconectar",
    command=conectar
).pack(side="left", padx=5)

tk.Label(
    barra, textvariable=estado,
    bg="#10231e", fg="#80d9a0"
).pack(side="left", padx=10)

panel = tk.Frame(ventana, bg="#10231e")
panel.pack(fill="x", padx=20)

for columna in range(4):
    panel.columnconfigure(columna, weight=1)


def tarjeta(titulo, columna, color):
    marco = tk.Frame(panel, bg="#19372e")
    marco.grid(
        row=0, column=columna,
        padx=6, pady=8, sticky="nsew"
    )

    tk.Label(
        marco, text=titulo,
        bg="#19372e", fg="white",
        font=("Arial", 12)
    ).pack(pady=10)

    valor = tk.Label(
        marco, text="--",
        bg="#19372e", fg=color,
        font=("Arial", 22, "bold")
    )
    valor.pack(pady=15)

    return valor


temp_label = tarjeta("Temperatura", 0, "#ffb777")
hum_label = tarjeta("Humedad del suelo", 1, "#72c9ff")
fan_label = tarjeta("Ventilador", 2, "#80d9a0")
pump_label = tarjeta("Bomba de agua", 3, "#80d9a0")

figura = Figure(figsize=(9, 3), facecolor="#19372e")
grafica = figura.add_subplot(111)

canvas = FigureCanvasTkAgg(figura, master=ventana)
canvas.get_tk_widget().pack(
    fill="both", expand=True, padx=25, pady=10
)

registro = tk.Label(
    ventana,
    text="Esperando datos de Arduino...",
    bg="#10231e",
    fg="white",
    font=("Arial", 11)
)
registro.pack(pady=15)


def actualizar_grafica():
    grafica.clear()
    grafica.set_facecolor("#19372e")

    grafica.plot(
        list(temperaturas),
        color="#ffb777",
        label="Temperatura (C)"
    )

    grafica.plot(
        list(humedades),
        color="#72c9ff",
        label="Humedad (%)"
    )

    grafica.tick_params(colors="white")
    grafica.grid(alpha=0.2)
    grafica.legend(loc="upper left")
    grafica.set_ylim(0, 100)

    canvas.draw_idle()


def mostrar_datos(linea):
    try:
        datos = linea.split(",")

        if len(datos) != 4:
            return

        temperatura = float(datos[0])
        humedad = int(datos[1])
        ventilador = int(datos[2])
        bomba = int(datos[3])

        temp_label.config(
            text=f"{temperatura:.1f} C"
            if temperatura == temperatura
            else "Error"
        )

        hum_label.config(text=f"{humedad}%")

        fan_label.config(
            text="ENCENDIDO" if ventilador else "APAGADO",
            fg="#80d9a0" if ventilador else "#a0a0a0"
        )

        pump_label.config(
            text="ENCENDIDA" if bomba else "APAGADA",
            fg="#72c9ff" if bomba else "#a0a0a0"
        )

        temperaturas.append(temperatura)
        humedades.append(humedad)

        actualizar_grafica()

        hora = datetime.now().strftime("%H:%M:%S")
        registro.config(
            text=f"Ultima lectura: {hora} | Modo automatico"
        )

    except ValueError:
        pass


def recibir_datos():
    if arduino and arduino.is_open:
        try:
            cantidad = arduino.in_waiting

            if cantidad:
                buffer.extend(arduino.read(cantidad))

            while b"\n" in buffer:
                linea, _, resto = buffer.partition(b"\n")
                buffer[:] = resto

                mostrar_datos(
                    linea.decode(
                        "utf-8", errors="ignore"
                    ).strip()
                )

        except serial.SerialException:
            estado.set("Conexion perdida")
            arduino.close()

    ventana.after(200, recibir_datos)


def cerrar():
    if arduino and arduino.is_open:
        arduino.close()
    ventana.destroy()


actualizar_puertos()
actualizar_grafica()
recibir_datos()

ventana.protocol("WM_DELETE_WINDOW", cerrar)
ventana.mainloop()
