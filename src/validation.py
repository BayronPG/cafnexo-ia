"""Validación de entradas en la frontera de la aplicación."""

RANGOS = {
    "precio_cop": (6000, 15000),
    "costo_unitario_cop": (2500, 8000),
    "costos_fijos_cop": (2_000_000, 15_000_000),
    "inflacion_pct": (0, 20),
    "promocion_cop": (0, 3_000_000),
    "trm_cop_usd": (3000, 6000),
}
TEMPORADAS = ("Baja", "Normal", "Alta")


def validar_entradas(e: dict) -> list[str]:
    """Devuelve la lista de errores; vacía si las entradas son válidas."""
    errores = []
    for campo, (lo, hi) in RANGOS.items():
        v = e.get(campo)
        if v is None or v == "":
            errores.append(f"{campo}: campo vacío.")
        elif not isinstance(v, (int, float)) or isinstance(v, bool):
            errores.append(f"{campo}: debe ser numérico.")
        elif v < 0:
            errores.append(f"{campo}: no se aceptan valores negativos.")
        elif not lo <= v <= hi:
            errores.append(f"{campo}: fuera del rango permitido ({lo:,} – {hi:,}).".replace(",", "."))
    if e.get("temporada") not in TEMPORADAS:
        errores.append("temporada: debe ser Baja, Normal o Alta.")
    if e.get("usa_insumos_importados") not in (0, 1, True, False):
        errores.append("usa_insumos_importados: debe ser 0 o 1.")
    return errores
