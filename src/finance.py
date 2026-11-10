"""Cálculos económicos declarados (no son IA). Usan la demanda predicha por el modelo."""


def calcular(precio: float, costo_unitario: float, costos_fijos: float, demanda: int) -> dict:
    ingresos = precio * demanda
    margen_unitario = precio - costo_unitario
    costos_variables = costo_unitario * demanda
    costos_totales = costos_fijos + costos_variables
    utilidad = ingresos - costos_totales
    margen_pct = utilidad / ingresos * 100 if ingresos > 0 else None
    # Precio <= costo: no existe punto de equilibrio (cada venta pierde dinero)
    pe = -(-costos_fijos // margen_unitario) if margen_unitario > 0 else None  # techo entero
    pe = int(pe) if pe is not None else None
    return {
        "demanda": int(demanda),
        "ingresos": ingresos,
        "margen_unitario": margen_unitario,
        "costos_variables": costos_variables,
        "costos_fijos": costos_fijos,
        "costos_totales": costos_totales,
        "utilidad": utilidad,
        "margen_pct": margen_pct,
        "punto_equilibrio": pe,
        "holgura": int(demanda) - pe if pe is not None else None,
    }


def formato_cop(valor: float) -> str:
    signo = "-" if valor < 0 else ""
    return f"{signo}$ {abs(valor):,.0f}".replace(",", ".")
