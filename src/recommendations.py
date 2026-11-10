"""Capa económica explicable de riesgo y recomendaciones (reglas declaradas, no IA)."""
from src.finance import formato_cop

TRM_ALTA = 4500


def _n(v: int) -> str:
    return f"{v:,}".replace(",", ".")


def _p(v: float) -> str:
    return f"{v:.1f}".replace(".", ",")


def clasificar_riesgo(r: dict) -> tuple[str, list[str]]:
    """Devuelve ('Alto'|'Medio'|'Bajo', motivos)."""
    pe, m = r["punto_equilibrio"], r["margen_pct"]
    alto = []
    if r["margen_unitario"] <= 0:
        alto.append("el precio es menor o igual al costo unitario")
    if r["utilidad"] < 0:
        alto.append("la utilidad es negativa")
    if pe is not None and r["demanda"] < pe:
        alto.append("la demanda estimada no alcanza el punto de equilibrio")
    if m is None or m < 5:
        alto.append("el margen de utilidad es menor al 5 %")
    if alto:
        return "Alto", alto

    medio = []
    if m <= 15:
        medio.append("el margen está entre 5 % y 15 %")
    if r["holgura"] < 0.15 * pe:
        medio.append("la demanda supera el punto de equilibrio por menos del 15 %")
    if r["utilidad"] < 0.10 * r["costos_totales"]:
        medio.append("la utilidad es inferior al 10 % de los costos totales")
    if medio:
        return "Medio", medio
    return "Bajo", ["utilidad positiva, margen superior al 15 % y demanda holgada sobre el punto de equilibrio"]


def decision(riesgo: str) -> str:
    return {"Bajo": "Adoptar", "Medio": "Adoptar con precaución",
            "Alto": "Ajustar antes de implementar"}[riesgo]


def generar_recomendaciones(r: dict, e: dict, riesgo: str) -> list[str]:
    recs = []
    pe, dem = r["punto_equilibrio"], r["demanda"]
    if r["margen_unitario"] <= 0:
        recs.append(f"El precio ({formato_cop(e['precio_cop'])}) no supera el costo unitario "
                    f"({formato_cop(e['costo_unitario_cop'])}): cada bebida genera pérdida. "
                    "Aumente el precio o reduzca el costo antes de operar.")
    elif dem < pe:
        recs.append(f"La demanda estimada ({_n(dem)} uds.) queda {_n(pe - dem)} unidades por debajo del punto "
                    f"de equilibrio ({_n(pe)} uds.). Revise precio, promoción y costos fijos.")
    if riesgo == "Alto":
        recs.append(f"No adopte este escenario sin ajustes: la utilidad mensual estimada es "
                    f"{formato_cop(r['utilidad'])}.")
    elif riesgo == "Medio":
        recs.append(f"Utilidad positiva de {formato_cop(r['utilidad'])} con margen de {_p(r['margen_pct'])} %, "
                    f"pero con poca holgura ({_n(r['holgura'])} uds. sobre el equilibrio). Conserve el escenario "
                    "solo con seguimiento mensual de ventas y costos.")
    else:
        recs.append(f"Escenario sólido: margen de {_p(r['margen_pct'])} % y {_n(r['holgura'])} unidades sobre el "
                    "punto de equilibrio. Valide el precio con una prueba piloto antes de implementarlo.")
    if e["temporada"] == "Baja":
        recs.append("Temporada baja: mantenga una reserva de caja y enfoque la promoción en días y "
                    "franjas de menor afluencia.")
    if e["usa_insumos_importados"] and e["trm_cop_usd"] >= TRM_ALTA:
        recs.append(f"Con insumos importados y TRM de {formato_cop(e['trm_cop_usd'])} por dólar, el escenario es "
                    "sensible al tipo de cambio: evalúe proveedores nacionales o compras anticipadas.")
    if e["inflacion_pct"] >= 8:
        recs.append(f"La inflación supuesta ({_p(e['inflacion_pct'])} %) presiona costos y reduce la demanda "
                    "estimada: revise contratos de insumos y la política de precios.")
    return recs
