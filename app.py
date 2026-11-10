"""CaféNexo IA — Simulador académico de demanda, rentabilidad y riesgo (Medellín)."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.finance import calcular, formato_cop
from src.prediction import cargar_metricas, cargar_modelo, predecir_demanda
from src.recommendations import clasificar_riesgo, decision, generar_recomendaciones
from src.validation import validar_entradas

BASE = dict(precio_cop=9000, costo_unitario_cop=4200, costos_fijos_cop=6_500_000, inflacion_pct=5.5,
            temporada="Normal", promocion_cop=600_000, trm_cop_usd=4100, usa_insumos_importados=0)
COLOR_RIESGO = {"Bajo": "#1e9e5a", "Medio": "#e0a800", "Alto": "#d64545"}
ICONO_RIESGO = {"Bajo": "🟢", "Medio": "🟡", "Alto": "🔴"}

st.set_page_config(page_title="CaféNexo IA", page_icon="☕", layout="wide")


@st.cache_resource
def recursos():
    return cargar_modelo(), cargar_metricas()


def analizar(modelo, e: dict):
    demanda = predecir_demanda(modelo, e)
    r = calcular(e["precio_cop"], e["costo_unitario_cop"], e["costos_fijos_cop"], demanda)
    riesgo, motivos = clasificar_riesgo(r)
    return r, riesgo, motivos


def pct(v):
    return "N/A" if v is None else f"{v:.1f} %".replace(".", ",")


def unidades(v):
    return "N/A" if v is None else f"{v:,}".replace(",", ".")


modelo, metricas = recursos()

# 1. Encabezado
st.title("☕ CaféNexo IA")
st.markdown("**Simulador académico de demanda, rentabilidad y riesgo para café especial en Medellín**")
st.caption("Proyecto: CaféNexo Medellín · Municipio: Medellín, Antioquia · Usuario: propietario o "
           "administrador de una pequeña cafetería de café especial")
st.info("**Pregunta económica:** ¿Qué combinación de precio, costos y condiciones económicas permite alcanzar "
        "una demanda y rentabilidad sostenibles para CaféNexo Medellín?")
st.warning("⚠️ Herramienta académica y orientativa. Los datos de entrenamiento son **simulados**, no ventas "
           "reales. No garantiza rentabilidad ni reemplaza la decisión del administrador.")

# 2. Panel lateral
ESCENARIOS = {
    "Escenario base": BASE,
    "Prueba 1: favorable": dict(precio_cop=10000, costo_unitario_cop=3900, costos_fijos_cop=5_500_000,
                                inflacion_pct=4.5, temporada="Alta", promocion_cop=1_000_000, trm_cop_usd=4000,
                                usa_insumos_importados=0),
    "Prueba 2: presión de costos": dict(precio_cop=9000, costo_unitario_cop=5600, costos_fijos_cop=7_500_000,
                                        inflacion_pct=9.0, temporada="Normal", promocion_cop=400_000,
                                        trm_cop_usd=4700, usa_insumos_importados=1),
    "Prueba 3: crítico": dict(precio_cop=7000, costo_unitario_cop=6500, costos_fijos_cop=9_000_000,
                              inflacion_pct=12.0, temporada="Baja", promocion_cop=0, trm_cop_usd=5000,
                              usa_insumos_importados=1),
}


def widgets(e: dict) -> dict:
    return {**e, "usa_insumos_importados": bool(e["usa_insumos_importados"])}  # checkbox exige bool


def cargar_escenario():
    st.session_state.update(widgets(ESCENARIOS[st.session_state.escenario]))


if "escenario" not in st.session_state:  # primera carga: ?escenario=1|2|3 precarga una prueba (enlaces y capturas)
    n = st.query_params.get("escenario", "0")
    st.session_state.escenario = list(ESCENARIOS)[int(n) if n in ("0", "1", "2", "3") else 0]
    st.session_state.update(widgets(ESCENARIOS[st.session_state.escenario]))

st.sidebar.selectbox("Cargar escenario de ejemplo", list(ESCENARIOS), key="escenario",
                     on_change=cargar_escenario)
with st.sidebar.form("entradas"):
    st.header("Escenario")
    precio = st.number_input("Precio de venta por bebida (COP)", 6000, 15000, step=500, key="precio_cop")
    costo = st.number_input("Costo variable unitario (COP)", 2500, 8000, step=100, key="costo_unitario_cop")
    fijos = st.number_input("Costos fijos mensuales (COP)", 2_000_000, 15_000_000, step=100_000,
                            key="costos_fijos_cop")
    inflacion = st.slider("Inflación anual (%)", 0.0, 20.0, step=0.1, key="inflacion_pct")
    temporada = st.selectbox("Temporada", ["Baja", "Normal", "Alta"], key="temporada")
    promocion = st.number_input("Inversión mensual en promoción (COP)", 0, 3_000_000, step=100_000,
                                key="promocion_cop")
    importados = st.checkbox("Usa insumos importados", key="usa_insumos_importados")
    trm = st.number_input("TRM (COP por USD)", 3000, 6000, step=50, key="trm_cop_usd",
                          help="Variable contextual: solo afecta la estimación si se usan insumos importados.")
    st.form_submit_button("Analizar escenario", type="primary", width="stretch")

entradas = dict(precio_cop=precio, costo_unitario_cop=costo, costos_fijos_cop=fijos, inflacion_pct=inflacion,
                temporada=temporada, promocion_cop=promocion, trm_cop_usd=trm,
                usa_insumos_importados=int(importados))
errores = validar_entradas(entradas)
if errores:
    for err in errores:
        st.error(err)
    st.stop()

r, riesgo, motivos = analizar(modelo, entradas)
rb, riesgo_b, _ = analizar(modelo, BASE)
recs = generar_recomendaciones(r, entradas, riesgo)

if r["margen_unitario"] <= 0:
    st.error("🚨 Alerta crítica: el precio es menor o igual al costo unitario. No existe punto de equilibrio.")
if r["utilidad"] < 0:
    st.error(f"Los ingresos no cubren los costos totales: pérdida mensual de {formato_cop(-r['utilidad'])}.")

# 3. Resultados principales
st.subheader("Resultados principales")
c = st.columns(5)
c[0].metric("Demanda IA (uds/mes)", unidades(r["demanda"]),
            f"{unidades(r['demanda'] - rb['demanda'])} vs. base")
c[1].metric("Utilidad mensual", formato_cop(r["utilidad"]),
            formato_cop(r["utilidad"] - rb["utilidad"]) + " vs. base")
c[2].metric("Margen de utilidad", pct(r["margen_pct"]))
c[3].metric("Punto de equilibrio (uds)", unidades(r["punto_equilibrio"]))
c[4].markdown(
    f"<div style='background:{COLOR_RIESGO[riesgo]};color:white;padding:10px;border-radius:8px;"
    f"text-align:center'><div style='font-size:0.85rem'>Nivel de riesgo</div>"
    f"<div style='font-size:1.6rem;font-weight:700'>{riesgo}</div>"
    f"<div style='font-size:0.8rem'>{decision(riesgo)}</div></div>", unsafe_allow_html=True)

# Recomendación
st.subheader(f"{ICONO_RIESGO[riesgo]} Recomendación: {decision(riesgo)}")
st.markdown(f"**Motivos del riesgo {riesgo.lower()}:** " + "; ".join(motivos) + ".")
for rec in recs:
    st.markdown(f"- {rec}")
st.caption("La clasificación de riesgo y la recomendación son reglas económicas declaradas aplicadas sobre la "
           "demanda estimada por el modelo; no son una segunda IA. Valide antes de decidir.")

# 4. Explicación de IA
ce = metricas["comparacion"][metricas["modelo_elegido"]]
with st.expander("🤖 ¿Dónde está la IA? Modelo, entradas, métricas y limitaciones"):
    st.markdown(
        f"La **única parte de IA** es un modelo supervisado de regresión (scikit-learn) que estima la "
        f"demanda mensual. Modelo seleccionado automáticamente por menor MAE: **{metricas['modelo_elegido']}**.")
    st.markdown(f"**Predicción para este escenario:** {unidades(r['demanda'])} bebidas/mes.")
    st.dataframe(pd.DataFrame([{k: v for k, v in entradas.items() if k != "costos_fijos_cop"}]),
                 hide_index=True, width="stretch")
    st.caption("Los costos fijos no son variable del modelo; se usan solo en los cálculos financieros. "
               "Si no hay insumos importados, la TRM se fija en el valor base (4.100) para la predicción.")
    comp = pd.DataFrame(metricas["comparacion"]).T.rename_axis("Modelo").reset_index()
    st.markdown("**Métricas en conjunto de prueba** (60 registros simulados):")
    st.dataframe(comp, hide_index=True, width="stretch")
    st.markdown(f"MAE = {ce['MAE']} uds · RMSE = {ce['RMSE']} uds · R² = {ce['R2']}")
    st.markdown("""**Limitaciones**
- El modelo es académico y orientativo.
- Los datos iniciales son simulados, no ventas reales.
- Una buena métrica sobre datos simulados no demuestra desempeño comercial real.
- La demanda real puede cambiar por competencia, clima, ubicación, calidad, eventos y preferencias no incluidas.
- La recomendación no reemplaza la validación del administrador.""")

# 5. Resultado financiero
st.subheader("Resultado financiero")
tabla = pd.DataFrame([
    ("Demanda estimada", "Predicción del modelo de IA", f"{unidades(r['demanda'])} uds"),
    ("Ingresos", "Precio × Demanda", formato_cop(r["ingresos"])),
    ("Margen unitario", "Precio − Costo variable unitario", formato_cop(r["margen_unitario"])),
    ("Costos variables", "Costo unitario × Demanda", formato_cop(r["costos_variables"])),
    ("Costos fijos", "Dato de entrada", formato_cop(r["costos_fijos"])),
    ("Costos totales", "Costos fijos + Costos variables", formato_cop(r["costos_totales"])),
    ("Utilidad", "Ingresos − Costos totales", formato_cop(r["utilidad"])),
    ("Margen porcentual", "Utilidad ÷ Ingresos × 100", pct(r["margen_pct"])),
    ("Punto de equilibrio", "Costos fijos ÷ Margen unitario", f"{unidades(r['punto_equilibrio'])} uds"),
    ("Holgura", "Demanda − Punto de equilibrio", f"{unidades(r['holgura'])} uds"),
], columns=["Concepto", "Fórmula", "Resultado"])
st.dataframe(tabla, hide_index=True, width="stretch")

# 6. Gráficos
g1, g2 = st.columns(2)
with g1:
    conceptos = ["Ingresos", "Costos variables", "Costos fijos", "Utilidad"]
    valores = [r["ingresos"], r["costos_variables"], r["costos_fijos"], r["utilidad"]]
    colores = ["#2b6cb0", "#dd8a3e", "#8c6d4f", "#1e9e5a" if r["utilidad"] >= 0 else "#d64545"]
    fig = go.Figure(go.Bar(x=conceptos, y=valores, marker_color=colores,
                           text=[formato_cop(v) for v in valores], textposition="outside"))
    fig.update_layout(title="Ingresos, costos y utilidad mensual", yaxis_title="COP", xaxis_title="Concepto",
                      height=420, margin=dict(t=60, b=40))
    st.plotly_chart(fig, width="stretch")
with g2:
    precios = list(range(6000, 15001, 500))
    utilidades = [analizar(modelo, {**entradas, "precio_cop": p})[0]["utilidad"] for p in precios]
    fig2 = go.Figure(go.Scatter(x=precios, y=utilidades, mode="lines+markers", name="Utilidad prevista",
                                line=dict(color="#6b4226")))
    fig2.add_trace(go.Scatter(x=[precio], y=[r["utilidad"]], mode="markers", name="Precio actual",
                              marker=dict(size=14, color=COLOR_RIESGO[riesgo], symbol="diamond")))
    fig2.add_hline(y=0, line_dash="dash", line_color="gray")
    fig2.update_layout(title="Sensibilidad de la utilidad al precio", xaxis_title="Precio por bebida (COP)",
                       yaxis_title="Utilidad mensual (COP)", height=420, margin=dict(t=60, b=40))
    st.plotly_chart(fig2, width="stretch")
    mejor = precios[max(range(len(precios)), key=utilidades.__getitem__)]
    st.caption(f"Manteniendo las demás variables, la mayor utilidad estimada se obtiene con un precio de "
               f"{formato_cop(mejor)}. Es una referencia orientativa, no un precio óptimo garantizado.")

# 7. Comparación con escenario base
st.subheader("Comparación con el escenario base")


def fila(nombre, actual, base, fmt):
    if actual is None or base is None:
        return (nombre, fmt(base), fmt(actual), "N/A", "N/A")
    dif = actual - base
    return (nombre, fmt(base), fmt(actual), fmt(dif), pct(dif / abs(base) * 100) if base else "N/A")


comparacion = pd.DataFrame([
    fila("Demanda (uds)", r["demanda"], rb["demanda"], unidades),
    fila("Utilidad (COP)", r["utilidad"], rb["utilidad"], formato_cop),
    ("Margen (%)", pct(rb["margen_pct"]), pct(r["margen_pct"]),
     "N/A" if r["margen_pct"] is None else f"{r['margen_pct'] - rb['margen_pct']:+.1f}".replace(".", ",") + " p.p.",
     "—"),
], columns=["Indicador", "Base", "Escenario actual", "Diferencia absoluta", "Diferencia %"])
st.dataframe(comparacion, hide_index=True, width="stretch")
st.caption(f"Escenario base: precio $ 9.000, costo $ 4.200, fijos $ 6.500.000, inflación 5,5 %, temporada "
           f"Normal, promoción $ 600.000, sin insumos importados. Riesgo base: {riesgo_b}.")

# 8. Fuentes y transparencia
st.subheader("Fuentes y transparencia")
t1, t2, t3, t4 = st.tabs(["Fuentes institucionales", "Supuestos académicos", "Datos simulados", "Limitaciones"])
with t1:
    st.markdown("""Referencias recomendadas para contrastar los supuestos. **No son el origen del conjunto
sintético** y no se les atribuyen cifras de esta app.
- DANE: https://www.dane.gov.co/
- Banco de la República: https://www.banrep.gov.co/es/estadisticas
- DNP / TerriData: https://terridata.dnp.gov.co/
- Superintendencia Financiera: https://www.superfinanciera.gov.co/
- DIAN: https://www.dian.gov.co/
- Ministerio de Comercio, Industria y Turismo: https://www.mincit.gov.co/""")
with t2:
    st.markdown("""Todos los valores base y rangos (precio, costo unitario, costos fijos, inflación, promoción
y TRM) son **supuestos académicos editables**, no cifras oficiales ni resultados de una empresa real.
La inversión en promoción se trata como variable de demanda y se asume incluida en los costos fijos mensuales.""")
with t3:
    st.markdown(f"""- Archivo: `data/datos_demanda.csv` · 300 registros · origen: **Simulado académico** (semilla 42).
- Entrenamiento: {metricas['registros_entrenamiento']} registros · prueba: {metricas['registros_prueba']}.
- Fecha de entrenamiento del modelo: {metricas['fecha_entrenamiento']}.
- *Datos simulados con fines académicos. No representan ventas reales del negocio.*""")
with t4:
    st.markdown("""- Estimación académica orientativa, no predicción empresarial exacta.
- No incluye competencia, clima, ubicación, calidad del producto, eventos ni preferencias.
- Las métricas se obtienen sobre datos simulados; no prueban desempeño comercial real.
- Fuera de los rangos de entrenamiento el modelo no es confiable (la app los bloquea).
- La app no almacena entradas, no pide datos personales y no usa APIs externas.""")
