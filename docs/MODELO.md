# Modelo de IA — estimación de demanda

## Qué es IA y qué no

| Componente | ¿Es IA? | Archivo |
|---|---|---|
| Estimación de demanda mensual | **Sí**: modelo supervisado de regresión (scikit-learn) | `src/prediction.py`, `train_model.py` |
| Ingresos, costos, utilidad, margen, equilibrio | No: fórmulas declaradas | `src/finance.py` |
| Nivel de riesgo y recomendación | No: reglas económicas explicables | `src/recommendations.py` |

## Datos

`data/datos_demanda.csv`: 300 registros **Simulado académico**, generados con `generate_data.py` (semilla 42).
La ecuación generadora solo crea datos de entrenamiento plausibles. El modelo no la conoce: la aprende de los datos.

## Variables

- **Objetivo:** `demanda_unidades`.
- **Predictoras:** `precio_cop`, `costo_unitario_cop`, `inflacion_pct`, `temporada`, `promocion_cop`, `trm_cop_usd`, `usa_insumos_importados`.
- **Derivada:** `trm_importado = trm_cop_usd × usa_insumos_importados`. Permite que la TRM pese solo cuando hay insumos importados.

## Pipeline

```text
FunctionTransformer (interacción TRM × importados)
  → ColumnTransformer
      numéricas:  SimpleImputer(mediana) → StandardScaler
      categórica: SimpleImputer(moda)    → OneHotEncoder
  → Regresor
```

Separación de los datos: 80 % para entrenamiento y 20 % para prueba (`random_state=42`). Se usa el mismo pipeline al entrenar y al predecir.

## Comparación y selección automática (menor MAE)

| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| **Regresión lineal** (elegido) | 43,34 | 57,27 | 0,9825 |
| Random Forest Regressor | 107,92 | 129,11 | 0,9110 |

Fuente: `models/metrics.json`. MAE = 43 uds significa que, en promedio, la estimación se desvía unas 43 bebidas al mes en los datos simulados de prueba.

La regresión lineal gana porque los datos simulados tienen una estructura casi lineal. Ese resultado **no prueba** que la demanda real sea lineal.

## Regenerar

```bash
python generate_data.py
python train_model.py
```
