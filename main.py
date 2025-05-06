import tkinter as tk
from tkinter import messagebox
import itertools
import re

OPERADORES = {"∧": " and ", "∨": " or ", "→": "<=", "↔": "==", "~": " not ", "⊕": "^"}


def evaluar_expresion(expresion, valores, variables):
    for i, valor in enumerate(valores):
        expresion = expresion.replace(variables[i], str(valor))

    for operador, python_operador in OPERADORES.items():
        expresion = expresion.replace(operador, python_operador)

    try:
        return eval(expresion)
    except:
        return None


def contar_variables(expresion):
    variables = set(re.findall(r"[p-t]", expresion))
    return list(variables)


def generar_tabla_verdad():
    expresion = entrada_expresion.get()

    if not expresion:
        messagebox.showerror("Error", "Por favor, ingrese una expresión lógica.")
        return

    variables_seleccionadas = contar_variables(expresion)

    if not variables_seleccionadas:
        messagebox.showerror(
            "Error",
            "La expresión debe contener algunas de las siguientes variables: p, q, r, s, t.",
        )
        return

    if len(variables_seleccionadas) > 5:
        messagebox.showerror(
            "Error", "La expresión no puede contener más de 5 variables."
        )
        return

    variables_seleccionadas.sort()
    if "p" in variables_seleccionadas:
        variables_seleccionadas.remove("p")
        variables_seleccionadas.insert(0, "p")
    if "q" in variables_seleccionadas:
        variables_seleccionadas.remove("q")
        variables_seleccionadas.insert(1, "q")

    combinaciones = list(
        itertools.product([True, False], repeat=len(variables_seleccionadas))
    )

    for widget in frame_resultados.winfo_children():
        widget.destroy()

    encabezados = variables_seleccionadas + [expresion]
    for col, encabezado in enumerate(encabezados):
        label = tk.Label(
            frame_resultados,
            text=encabezado,
            width=15,
            height=2,
            relief="solid",
            bg="#e0e0e0",
        )
        label.grid(row=0, column=col)

    for i, combinacion in enumerate(combinaciones):
        resultado = evaluar_expresion(expresion, combinacion, variables_seleccionadas)
        fila = [("V" if valor else "F") for valor in combinacion] + [
            ("V" if resultado else "F")
        ]
        for j, valor in enumerate(fila):
            label = tk.Label(
                frame_resultados,
                text=str(valor),
                width=15,
                height=2,
                relief="solid",
                bg="#f5f5f5",
            )
            label.grid(row=i + 1, column=j)


def agregar_operador(operador):
    entrada_expresion.insert(tk.END, operador)


def borrar_expresion():
    entrada_expresion.delete(0, tk.END)


ventana = tk.Tk()
ventana.title("Generador de Tabla de Verdad")

ventana.geometry("400x650")
ventana.config(bg="#000000")

frame_inputs = tk.Frame(ventana, bg="#FFFFFF")
frame_inputs.pack(pady=20)

tk.Label(
    frame_inputs, text="Expresión lógica:", bg="#FFFFFF", font=("Arial", 12)
).pack()
entrada_expresion = tk.Entry(frame_inputs, width=18, font=("Arial", 12))
entrada_expresion.pack(pady=10)

frame_variables = tk.Frame(ventana, bg="#FFFFFF")
frame_variables.pack(pady=10)

boton_p = tk.Button(
    frame_variables,
    text="p",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador("p"),
)
boton_p.grid(row=0, column=0, padx=5)

boton_q = tk.Button(
    frame_variables,
    text="q",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador("q"),
)
boton_q.grid(row=0, column=1, padx=5)

boton_r = tk.Button(
    frame_variables,
    text="r",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador("r"),
)
boton_r.grid(row=0, column=2, padx=5)

boton_s = tk.Button(
    frame_variables,
    text="s",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador("s"),
)
boton_s.grid(row=0, column=3, padx=5)

boton_t = tk.Button(
    frame_variables,
    text="t",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador("t"),
)
boton_t.grid(row=0, column=4, padx=5)

frame_operadores = tk.Frame(ventana, bg="#FFFFFF")
frame_operadores.pack(pady=10)

boton_negacion = tk.Button(
    frame_operadores,
    text="~",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador("~"),
)
boton_negacion.grid(row=0, column=0, padx=5)

boton_conjuncion = tk.Button(
    frame_operadores,
    text="∧",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador("∧"),
)
boton_conjuncion.grid(row=0, column=1, padx=5)

boton_disyuncion = tk.Button(
    frame_operadores,
    text="∨",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador("∨"),
)
boton_disyuncion.grid(row=0, column=2, padx=5)

boton_implicacion = tk.Button(
    frame_operadores,
    text="→",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador("→"),
)
boton_implicacion.grid(row=1, column=0, padx=5)

boton_bicondicional = tk.Button(
    frame_operadores,
    text="↔",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador("↔"),
)
boton_bicondicional.grid(row=1, column=1, padx=5)

boton_xor = tk.Button(
    frame_operadores,
    text="⊕",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador("⊕"),
)
boton_xor.grid(row=1, column=2, padx=5)

boton_parentesis_abrir = tk.Button(
    frame_operadores,
    text="(",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador("("),
)
boton_parentesis_abrir.grid(row=2, column=0, padx=5)

boton_parentesis_cerrar = tk.Button(
    frame_operadores,
    text=")",
    width=4,
    height=1,
    font=("Arial", 12),
    command=lambda: agregar_operador(")"),
)
boton_parentesis_cerrar.grid(row=2, column=1, padx=5)

boton_generar = tk.Button(
    frame_inputs,
    text="Generar Tabla de Verdad",
    command=generar_tabla_verdad,
    font=("Arial", 12),
    bg="#4CAF50",
    fg="white",
)
boton_generar.pack(pady=10)

boton_borrar = tk.Button(
    frame_inputs,
    text="Borrar Expresión",
    command=borrar_expresion,
    font=("Arial", 12),
    bg="#FF5722",
    fg="white",
)
boton_borrar.pack(pady=10)

frame_resultados = tk.Frame(ventana)
frame_resultados.pack(pady=20)

ventana.mainloop()
