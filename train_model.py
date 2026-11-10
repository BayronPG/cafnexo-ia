"""Entrena Regresión Lineal y Random Forest, elige el de menor MAE y guarda pipeline + métricas."""
import json
from datetime import date

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from src.prediction import (CATEGORICAS, NUMERICAS, PREDICTORAS, RAIZ, RUTA_METRICAS,
                            RUTA_MODELO, agregar_interaccion)

OBJETIVO = "demanda_unidades"


def construir_pipeline(regresor) -> Pipeline:
    pre = ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                          ("esc", StandardScaler())]), NUMERICAS),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("ohe", OneHotEncoder(handle_unknown="ignore"))]), CATEGORICAS),
    ])
    return Pipeline([("interaccion", FunctionTransformer(agregar_interaccion)),
                     ("pre", pre), ("modelo", regresor)])


def evaluar(y_real, y_pred) -> dict:
    return {"MAE": round(float(mean_absolute_error(y_real, y_pred)), 2),
            "RMSE": round(float(np.sqrt(mean_squared_error(y_real, y_pred))), 2),
            "R2": round(float(r2_score(y_real, y_pred)), 4)}


def entrenar():
    df = pd.read_csv(RAIZ / "data" / "datos_demanda.csv").drop_duplicates()
    X, y = df[PREDICTORAS], df[OBJETIVO]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    candidatos = {
        "Regresión lineal": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=300, random_state=42),
    }
    resultados, pipelines = {}, {}
    for nombre, reg in candidatos.items():
        pipe = construir_pipeline(reg).fit(X_tr, y_tr)
        resultados[nombre] = evaluar(y_te, pipe.predict(X_te))
        pipelines[nombre] = pipe

    elegido = min(resultados, key=lambda n: resultados[n]["MAE"])
    joblib.dump(pipelines[elegido], RUTA_MODELO)
    metricas = {
        "modelo_elegido": elegido,
        "criterio": "Menor MAE en conjunto de prueba (20 %, random_state=42)",
        "comparacion": resultados,
        "variables": PREDICTORAS,
        "variable_derivada": "trm_importado = trm_cop_usd × usa_insumos_importados",
        "objetivo": OBJETIVO,
        "registros_entrenamiento": len(X_tr),
        "registros_prueba": len(X_te),
        "origen_datos": "Simulado académico",
        "fecha_entrenamiento": date.today().isoformat(),
    }
    RUTA_METRICAS.write_text(json.dumps(metricas, ensure_ascii=False, indent=2), encoding="utf-8")
    return metricas


if __name__ == "__main__":
    print(json.dumps(entrenar(), ensure_ascii=False, indent=2))
