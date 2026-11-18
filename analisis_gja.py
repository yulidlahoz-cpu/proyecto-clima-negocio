
import pandas as pd

# Nombre del archivo Excel
archivo = "Proyecto_GJA_ el clima en mi negocio.xlsx"

# Leer las hojas del archivo
excel = pd.ExcelFile(archivo)

print("HOJAS DEL ARCHIVO:")
print(excel.sheet_names)

# Mostrar la primera hoja
df = pd.read_excel(archivo, sheet_name=0)

print("\nPRIMEROS REGISTROS:")
print(df.head())

print("\nCANTIDAD DE FILAS Y COLUMNAS:")
print(df.shape)

print("\nINFORMACIÓN DE LOS DATOS:")
df.info()

# ANALISIS DE LAS VENTAS DE GJA

# Total de pares vendidos
total_pares = df["Pares_vendidos"].sum()

# Total de ingresos
total_ingresos = df["Ingresos_COP"].sum()

# Promedio de pares vendidos por día
promedio_pares = df["Pares_vendidos"].mean()

# Promedio de ingresos por día
promedio_ingresos = df["Ingresos_COP"].mean()

# Día con mayores ingresos
dia_mayor_venta = df.loc[df["Ingresos_COP"].idxmax()]

# Mostrar resultados
print("\n===== RESULTADOS DE VENTAS GJA =====")

print("Total de pares vendidos:", total_pares)

print("Ingresos totales: $", total_ingresos)

print("Promedio de pares vendidos por día:", round(promedio_pares, 2))

print("Promedio de ingresos diarios: $", round(promedio_ingresos, 2))

print("Día con mayores ingresos:", dia_mayor_venta["Fecha"])
print("Valor de la mayor venta: $", dia_mayor_venta["Ingresos_COP"])


import matplotlib.pyplot as plt

# Preparar las fechas
df["Fecha"] = pd.to_datetime(df["Fecha"])

# GRAFICO 1: INGRESOS POR DIA
plt.figure(figsize=(10, 5))
plt.plot(df["Fecha"], df["Ingresos_COP"], marker="o")
plt.title("Ingresos diarios de GJA")
plt.xlabel("Fecha")
plt.ylabel("Ingresos (pesos)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("grafico_ventas.png")
plt.show()

# GRAFICO 2: TEMPERATURA Y PARES VENDIDOS
plt.figure(figsize=(8, 5))
plt.scatter(df["Temperatura_media_C"], df["Pares_vendidos"])
plt.title("Temperatura frente a pares vendidos")
plt.xlabel("Temperatura media (°C)")
plt.ylabel("Pares vendidos")
plt.tight_layout()
plt.savefig("grafico_temperatura.png")
plt.show()

# GRAFICO 3: LLUVIA Y PROMEDIO DE PARES VENDIDOS
promedio_lluvia = df.groupby("Llovio")["Pares_vendidos"].mean()

plt.figure(figsize=(7, 5))
promedio_lluvia.plot(kind="bar")
plt.title("Promedio de pares vendidos según lluvia")
plt.xlabel("¿Llovió?")
plt.ylabel("Promedio de pares vendidos")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("grafico_lluvia.png")
plt.show()

print("Los tres gráficos fueron creados correctamente.")

