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

    # Aplicar la deducción de ganancias no imponibles
    deduccion_ganancias_no_imponibles = 257586.25
    deduccion_especial_incrementada_mensual = 1236414 / 12  # Ajustar según corresponda

    ganancia_neta_sujeta_impuesto = max(0, sueldo_neto_mensual - deduccion_ganancias_no_imponibles - deduccion_especial_incrementada_mensual)

    impuesto_ganancias = calcular_impuesto_ganancias(ganancia_neta_sujeta_impuesto)

    sueldo_neto_final = sueldo_neto_mensual - impuesto_ganancias

    return round(sueldo_neto_final), round(jubilacion), round(obra_social), round(pami), round(impuesto_ganancias)

st.title('Calculadora de Sueldo Neto en Argentina - 2024')

sueldo_bruto = st.number_input('Ingrese su sueldo bruto en ARS', min_value=0.0, step=1000.0)

if st.button('Calcular'):
    sueldo_neto_final, jubilacion, obra_social, pami, impuesto_ganancias = calcular_sueldo_neto(sueldo_bruto)
    st.write(f'**El sueldo neto es: ARS {sueldo_neto_final:,}**')
    st.write('**Detalle de deducciones:**')
    st.write(f'- **Jubilación:** ARS {jubilacion:,}')
    st.write(f'- **Obra Social:** ARS {obra_social:,}')
    st.write(f'- **PAMI:** ARS {pami:,}')
    st.write(f'- **Impuesto a las Ganancias:** ARS {impuesto_ganancias:,}')
