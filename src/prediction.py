"""Carga del modelo de IA y predicción de demanda."""
import json
from pathlib import Path

import joblib
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
RUTA_MODELO = RAIZ / "models" / "demand_model.joblib"
RUTA_METRICAS = RAIZ / "models" / "metrics.json"
TRM_BASE = 4100

NUMERICAS = ["precio_cop", "costo_unitario_cop", "inflacion_pct", "promocion_cop",
             "trm_cop_usd", "usa_insumos_importados", "trm_importado"]
CATEGORICAS = ["temporada"]
PREDICTORAS = ["precio_cop", "costo_unitario_cop", "inflacion_pct", "temporada",
               "promocion_cop", "trm_cop_usd", "usa_insumos_importados"]


def agregar_interaccion(df: pd.DataFrame) -> pd.DataFrame:
    """La TRM solo pesa cuando hay insumos importados: variable derivada TRM × importados."""
    df = df.copy()
    df["trm_importado"] = df["trm_cop_usd"] * df["usa_insumos_importados"]
    return df


def cargar_modelo(ruta=RUTA_MODELO):
    return joblib.load(ruta)


def cargar_metricas(ruta=RUTA_METRICAS) -> dict:
    return json.loads(Path(ruta).read_text(encoding="utf-8"))


def predecir_demanda(modelo, entradas: dict) -> int:
    fila = {k: entradas[k] for k in PREDICTORAS}
    fila["usa_insumos_importados"] = int(fila["usa_insumos_importados"])
    if not fila["usa_insumos_importados"]:
        fila["trm_cop_usd"] = TRM_BASE  # TRM contextual: solo afecta con insumos importados
    pred = float(modelo.predict(pd.DataFrame([fila]))[0])
    return max(0, round(pred))
