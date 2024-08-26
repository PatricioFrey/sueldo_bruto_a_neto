import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def calcular_impuesto_ganancias(ganancia_neta_sujeta_impuesto):

    # Libero los casos que es 0
    if ganancia_neta_sujeta_impuesto == 0:
        return 0

    # Actualizar de https://www.afip.gob.ar/gananciasYBienes/ganancias/sujetos/empleados-y-jubilados/documentos/Ganancias-Escala-PH-2024.pdf
    tramos = [
        (0, 419253.95, 0.05, 0),
        (419253.95, 838507.92, 0.09, 20962.70),
        (838507.92, 1257761.87, 0.12, 58695.55),
        (1257761.87, 1677015.87, 0.15, 109006.03),
        (1677015.87, 2515523.74, 0.19, 171894.13),
        (2515523.74, 3354031.63, 0.23, 331210.62),
        (3354031.63, 5031047.45, 0.27, 524067.44),
        (5031047.45, 6708063.39, 0.31, 976861.71),
        (6708063.39, float('inf'), 0.35, 1496736.65)
    ]

    impuesto = 0
    for tramo in tramos:
        if (ganancia_neta_sujeta_impuesto > tramo[0]) and (ganancia_neta_sujeta_impuesto <= tramo[1]):
            excedente_del_tramo = ganancia_neta_sujeta_impuesto - tramo[0]
            impuesto += excedente_del_tramo * tramo[2] + tramo[3]
            break

    return round(impuesto)

def calcular_sueldo_neto(sueldo_bruto):
    base_maxima = 2467787

    base_imponible = min(sueldo_bruto, base_maxima)

    jubilacion = 0.11 * base_imponible
    obra_social = 0.03 * base_imponible
    pami = 0.03 * base_imponible

    sueldo_neto_mensual = sueldo_bruto - (jubilacion + obra_social + pami)

    deduccion_ganancias_no_imponibles = 257586.25
    deduccion_especial_incrementada_mensual = 1236414 / 12

    ganancia_neta_sujeta_impuesto = max(0, sueldo_neto_mensual - deduccion_ganancias_no_imponibles - deduccion_especial_incrementada_mensual)

    impuesto_ganancias = calcular_impuesto_ganancias(ganancia_neta_sujeta_impuesto)

    sueldo_neto_final = sueldo_neto_mensual - impuesto_ganancias

    return round(sueldo_neto_final), round(jubilacion), round(obra_social), round(pami), round(impuesto_ganancias)

# Streamlit UI
st.title('Calculadora de Sueldo Neto y Gráfico de Relación - 2024')

# Entrada del usuario para sueldo bruto
sueldo_bruto_ingresado = st.number_input('Ingrese su sueldo bruto en ARS', min_value=300000.0, step=1000.0)

# Calcular y mostrar el detalle del sueldo neto
if sueldo_bruto_ingresado:
    sueldo_neto, jubilacion, obra_social, pami, impuesto_ganancias = calcular_sueldo_neto(sueldo_bruto_ingresado)
    st.subheader('Detalle del Cálculo')
    st.write(f'- **Sueldo Bruto:** ARS {sueldo_bruto_ingresado:,.2f}')
    st.write(f'- **Jubilación (11%):** ARS {jubilacion:,.2f}')
    st.write(f'- **Obra Social (3%):** ARS {obra_social:,.2f}')
    st.write(f'- **PAMI (3%):** ARS {pami:,.2f}')
    st.write(f'- **Impuesto a las Ganancias:** ARS {impuesto_ganancias:,.2f}')
    st.write(f'- **Sueldo Neto:** ARS {sueldo_neto:,.2f}')

# Generar valores de sueldo bruto para el gráfico
sueldos_brutos = np.linspace(300000, 20000000, 500)
sueldos_netos = [calcular_sueldo_neto(sueldo)[0] for sueldo in sueldos_brutos]

# Crear el gráfico
plt.figure(figsize=(12, 8))
plt.plot(sueldos_brutos, sueldos_netos, label="Sueldo Neto vs Sueldo Bruto", color='dodgerblue', linewidth=2)

# Añadir detalles adicionales
plt.title("Sueldo Neto en función del Sueldo Bruto (2024)", fontsize=16, fontweight='bold')
plt.xlabel("Sueldo Bruto (ARS)", fontsize=14)
plt.ylabel("Sueldo Neto (ARS)", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Añadir anotaciones para destacar puntos clave
for i, sueldo_bruto in enumerate([300000, 5000000, 10000000, 15000000, 20000000]):
    sueldo_neto = calcular_sueldo_neto(sueldo_bruto)[0]
    plt.annotate(f'Bruto: ${sueldo_bruto:,}\nNeto: ${sueldo_neto:,}', 
                 xy=(sueldo_bruto, sueldo_neto), 
                 xytext=(sueldo_bruto, sueldo_neto + 100000),
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 fontsize=10, color='darkred')

# Añadir una leyenda
plt.legend(fontsize=12)

# Añadir un fondo de color claro
plt.gca().set_facecolor('#f7f7f7')

# Añadir una descripción en la parte inferior
plt.figtext(0.5, -0.05, "Este gráfico muestra cómo el sueldo neto se ve afectado por el aumento del sueldo bruto, considerando las deducciones y el impuesto a las ganancias.", 
            ha="center", fontsize=12, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

plt.tight_layout()

# Mostrar el gráfico en Streamlit
st.pyplot(plt)
