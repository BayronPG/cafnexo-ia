# CaféNexo IA

**CaféNexo Medellín: simulador inteligente de demanda y rentabilidad para café especial**
Entregable 5: aplicación web con inteligencia artificial · Medellín, Antioquia, Colombia.

> URL pública: _pendiente de despliegue (ver sección 13)_ · Respaldo: `05_Aplicacion_IA.zip`

## 1. Problema
La cafetería debe fijar un precio que cubra los costos y conserve suficiente demanda. Un precio bajo puede elevar las ventas y aun así generar pérdidas. Uno alto mejora el margen por unidad, pero reduce la demanda.

**Pregunta central:** ¿qué combinación de precio, costos y condiciones económicas permite alcanzar una demanda y rentabilidad sostenibles para CaféNexo Medellín?

## 2. Usuario objetivo
Propietario o administrador de una pequeña cafetería de café especial en Medellín. La app le ayuda a decidir si un escenario se **adopta**, se **adopta con precaución** o se **ajusta antes de implementarse**.

## 3. Funcionalidades
- 7 entradas editables: precio, costo unitario, costos fijos, inflación, temporada, promoción y TRM (activa solo con insumos importados).
- Escenarios precargados (Base y Pruebas 1–3) en un selector, o en la URL con `?escenario=0..3`.
- Demanda mensual estimada por IA y comparación con el escenario base.
- Ingresos, costos variables y totales, utilidad, margen, margen unitario, punto de equilibrio y holgura.
- Riesgo bajo, medio o alto con colores, y una recomendación con cifras concretas.
- Gráficos de barras (ingresos, costos y utilidad) y de sensibilidad de la utilidad al precio.
- Sección de transparencia: fuentes, supuestos, datos simulados y limitaciones.

## 4. La IA
Modelo supervisado de regresión de scikit-learn que estima `demanda_unidades`. Se entrenan una **Regresión lineal** y un **Random Forest**, y se elige automáticamente el de menor MAE en el conjunto de prueba.

| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| **Regresión lineal (elegido)** | 43,34 | 57,27 | 0,9825 |
| Random Forest | 107,92 | 129,11 | 0,9110 |

Detalle en [docs/MODELO.md](docs/MODELO.md).

## 5. Predicción frente a cálculos económicos
**La IA es únicamente la estimación de demanda.** Todo lo demás son fórmulas declaradas que se aplican sobre esa demanda:

```text
Ingresos = Precio × Demanda estimada
Margen unitario = Precio − Costo variable unitario
Costos variables = Costo variable unitario × Demanda estimada
Costos totales = Costos fijos + Costos variables
Utilidad = Ingresos − Costos totales
Margen % = Utilidad / Ingresos × 100
Punto de equilibrio = Costos fijos / Margen unitario   (redondeado hacia arriba)
Holgura = Demanda estimada − Punto de equilibrio
```

El riesgo y la recomendación también son reglas económicas explicables (`src/recommendations.py`), no una segunda IA.

## 6. Origen y clasificación de los datos
| Dato | Clasificación |
|---|---|
| `data/datos_demanda.csv` (300 registros) | **Simulado académico** (semilla 42). No son ventas reales |
| Valores base y rangos de entrada | **Supuesto académico** editable |
| Enlaces DANE, BanRep, etc. | Referencias recomendadas, **no** origen de los datos |

> Datos simulados con fines académicos. No representan ventas reales del negocio.

Escenario base: precio $ 9.000 · costo $ 4.200 · fijos $ 6.500.000 · inflación 5,5 % · Normal · promoción $ 600.000 · TRM 4.100 · sin importados.

## 7. Instalación
Requiere Python 3.11.

```bash
python -m venv .venv
```
macOS / Linux: `source .venv/bin/activate` · Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
```bash
pip install -r requirements.txt
```

## 8. Ejecución
```bash
streamlit run app.py
```
Abrir `http://localhost:8501`.

## 9. Regenerar los datos
```bash
python generate_data.py
```

## 10. Entrenar el modelo
```bash
python train_model.py
```
Genera `models/demand_model.joblib` y `models/metrics.json`.

## 11. Pruebas
```bash
pytest -q
```
16 pruebas automatizadas. Las pruebas manuales están en [docs/PRUEBAS.md](docs/PRUEBAS.md) y las capturas en [docs/CAPTURAS.md](docs/CAPTURAS.md).

## 12. Tres casos demostrativos
| Caso | Demanda IA | Utilidad | Margen | Riesgo |
|---|---:|---:|---:|---|
| Base (`?escenario=0`) | 1.390 | $ 172.000 | 1,4 % | Alto |
| 1. Favorable (`?escenario=1`) | 1.589 | $ 4.192.900 | 26,4 % | Bajo |
| 2. Presión de costos (`?escenario=2`) | 1.252 | −$ 3.243.200 | −28,8 % | Alto |
| 3. Crítico (`?escenario=3`) | 1.124 | −$ 8.438.000 | −107,2 % | Alto |

## 13. Despliegue en Streamlit Community Cloud
1. Subir esta carpeta a un repositorio público de GitHub. Debe incluir `models/` y `data/`.
2. En https://share.streamlit.io: **Create app**, elegir el repositorio, la rama y el archivo `app.py`.
3. En *Advanced settings*, seleccionar **Python 3.11**.
4. Desplegar, abrir la URL en una ventana de incógnito y ejecutar los tres escenarios.
5. Copiar la URL en este README, el Word y el PowerPoint.

## 14. Limitaciones
Resumen: es una estimación académica entrenada con datos simulados y no considera competencia, clima, ubicación ni eventos. No garantiza rentabilidad. Ver [LIMITACIONES.md](LIMITACIONES.md).

## 15. Fuentes institucionales recomendadas
- DANE: https://www.dane.gov.co/
- Banco de la República: https://www.banrep.gov.co/es/estadisticas
- DNP / TerriData: https://terridata.dnp.gov.co/
- Superintendencia Financiera: https://www.superfinanciera.gov.co/
- DIAN: https://www.dian.gov.co/
- MinCIT: https://www.mincit.gov.co/

Ninguna cifra de la app proviene de estas fuentes. Si se incorporan cifras reales, se debe registrar la fecha de consulta.

## 16. Dependencias y costos
Software libre y gratuito: Streamlit, pandas, numpy, scikit-learn, joblib, plotly y pytest (versiones fijadas en `requirements.txt`). **No usa APIs pagas, no requiere claves y no almacena datos personales.**

## Estructura
```text
app.py  generate_data.py  train_model.py  requirements.txt
data/datos_demanda.csv   models/{demand_model.joblib, metrics.json}
src/{finance, prediction, recommendations, validation}.py
tests/   docs/{PRUEBAS, MODELO, CAPTURAS}.md + docs/capturas/
```
