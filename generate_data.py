"""Genera el dataset sintético de demanda (Simulado académico) con semilla 42."""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_REGISTROS = 300
RUIDO_SD = 65  # dentro del rango 55–80 definido en el contexto maestro
RUTA = Path(__file__).parent / "data" / "datos_demanda.csv"
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
         "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
EFECTO_TEMPORADA = {"Baja": -180, "Normal": 0, "Alta": 220}


def _paso(rng, lo, hi, paso, n):
    return lo + rng.integers(0, int((hi - lo) / paso) + 1, n) * paso


def generar(n=N_REGISTROS, seed=SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "mes": [MESES[i % 12] for i in range(n)],
        "precio_cop": _paso(rng, 6000, 15000, 500, n),
        "costo_unitario_cop": _paso(rng, 2500, 8000, 100, n),
        "inflacion_pct": np.round(rng.uniform(0, 20, n), 1),
        "temporada": rng.choice(["Baja", "Normal", "Alta"], n, p=[0.3, 0.45, 0.25]),
        "promocion_cop": _paso(rng, 0, 3_000_000, 100_000, n),
        "trm_cop_usd": _paso(rng, 3000, 6000, 50, n),
        "usa_insumos_importados": rng.integers(0, 2, n),
    })
    demanda = (
        1250
        - 0.11 * (df.precio_cop - 9000)
        - 18 * (df.inflacion_pct - 5.5)
        + 0.00022 * df.promocion_cop
        + df.temporada.map(EFECTO_TEMPORADA)
        - 0.055 * (df.trm_cop_usd - 4100) * df.usa_insumos_importados
        + rng.normal(0, RUIDO_SD, n)
    )
    df["demanda_unidades"] = np.maximum(100, demanda).round().astype(int)
    df["origen_dato"] = "Simulado académico"
    return df


def validar(df: pd.DataFrame) -> None:
    assert len(df) == N_REGISTROS and not df.isna().any().any()
    assert df.precio_cop.between(6000, 15000).all()
    assert df.costo_unitario_cop.between(2500, 8000).all()
    assert df.inflacion_pct.between(0, 20).all()
    assert df.promocion_cop.between(0, 3_000_000).all()
    assert df.trm_cop_usd.between(3000, 6000).all()
    assert set(df.temporada) <= {"Baja", "Normal", "Alta"}
    assert set(df.usa_insumos_importados) <= {0, 1}
    assert (df.demanda_unidades >= 100).all()


if __name__ == "__main__":
    datos = generar()
    validar(datos)
    RUTA.parent.mkdir(exist_ok=True)
    datos.to_csv(RUTA, index=False)
    print(f"{len(datos)} registros -> {RUTA}")
    print(datos.describe().round(1).to_string())
