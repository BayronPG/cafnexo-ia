# Pruebas documentadas — CaféNexo IA

Ejecutadas el 2026-11-09 con el modelo entrenado en esa fecha (Regresión lineal, semilla 42).
Los valores se obtuvieron **ejecutando la aplicación**; no fueron escritos de antemano.
Cada escenario se reproduce desde el selector «Cargar escenario de ejemplo» o con la URL `?escenario=N`.

Referencia, escenario base (`?escenario=0`): demanda 1.390 uds · utilidad $ 172.000 · margen 1,4 % ·
punto de equilibrio 1.355 uds · riesgo **Alto** (margen < 5 %). Captura: `docs/capturas/escenario_0.png`.

---

## Prueba 1: escenario favorable

- **Objetivo:** verificar que un precio mayor, costos controlados y temporada alta producen una utilidad positiva y un riesgo bajo.
- **Entradas:** precio $ 10.000 · costo unitario $ 3.900 · costos fijos $ 5.500.000 · inflación 4,5 % · temporada Alta · promoción $ 1.000.000 · TRM 4.000 · insumos importados: No.
- **Respuesta obtenida:**

| Indicador | Resultado |
|---|---:|
| Demanda estimada (IA) | 1.589 uds/mes (+199 vs. base) |
| Ingresos | $ 15.890.000 |
| Utilidad | $ 4.192.900 (+$ 4.020.900 vs. base) |
| Margen | 26,4 % |
| Punto de equilibrio | 902 uds |
| Holgura | 687 uds |
| Riesgo / decisión | **Bajo**: adoptar |

- **Interpretación económica:** la demanda supera en un 76 % el punto de equilibrio. El margen unitario de $ 6.100 cubre los costos fijos con amplitud. La app recomienda validar el precio con una prueba piloto.
- **Resultado esperado:** predicción visible, utilidad positiva, explicación y comparación con la base. ✔
- **Estado:** ✅ Aprobada
- **Captura:** `docs/capturas/escenario_1.png`

---

## Prueba 2: presión de costos

- **Objetivo:** verificar que el aumento del costo unitario, de la inflación y de la TRM (con insumos importados) reduce el margen y eleva el riesgo.
- **Entradas:** precio $ 9.000 · costo unitario $ 5.600 · costos fijos $ 7.500.000 · inflación 9 % · temporada Normal · promoción $ 400.000 · TRM 4.700 · insumos importados: Sí.
- **Respuesta obtenida:**

| Indicador | Resultado |
|---|---:|
| Demanda estimada (IA) | 1.252 uds/mes (−138 vs. base) |
| Ingresos | $ 11.268.000 |
| Utilidad | −$ 3.243.200 |
| Margen | −28,8 % (−30,2 p.p. vs. base) |
| Punto de equilibrio | 2.206 uds |
| Holgura | −954 uds |
| Riesgo / decisión | **Alto**: ajustar antes de implementar |

- **Interpretación económica:** el margen unitario cae a $ 3.400. Con costos fijos más altos, el equilibrio sube a 2.206 unidades. Además, la inflación y la TRM reducen la demanda estimada, así que la rentabilidad es muy sensible a los insumos. La app advierte sobre la TRM y la inflación.
- **Resultado esperado:** margen menor, advertencia por costos y TRM, y riesgo medio o alto. ✔ (alto)
- **Estado:** ✅ Aprobada
- **Captura:** `docs/capturas/escenario_2.png`

---

## Prueba 3: escenario crítico

- **Objetivo:** verificar la alerta roja cuando el precio bajo, los costos altos y la temporada baja hacen inviable la operación.
- **Entradas:** precio $ 7.000 · costo unitario $ 6.500 · costos fijos $ 9.000.000 · inflación 12 % · temporada Baja · promoción $ 0 · TRM 5.000 · insumos importados: Sí.
- **Respuesta obtenida:**

| Indicador | Resultado |
|---|---:|
| Demanda estimada (IA) | 1.124 uds/mes (−266 vs. base) |
| Ingresos | $ 7.868.000 |
| Utilidad | −$ 8.438.000 |
| Margen | −107,2 % |
| Margen unitario | $ 500 |
| Punto de equilibrio | 18.000 uds |
| Riesgo / decisión | **Alto**: ajustar antes de implementar |

- **Interpretación económica:** con $ 500 de margen por bebida se necesitarían 18.000 unidades al mes. La demanda estimada es 16 veces menor. El volumen no cubre los costos totales. La app recomienda no adoptar el escenario, mantener reserva de caja y revisar la exposición cambiaria.
- **Resultado esperado:** margen unitario muy bajo, utilidad negativa, riesgo alto y recomendación de no adoptar sin ajustes. ✔
- **Estado:** ✅ Aprobada
- **Captura:** `docs/capturas/escenario_3.png`

---

## Pruebas automatizadas

`pytest -q` → **16 pruebas aprobadas**. Cubren fórmulas, precio ≤ costo, ingresos cero, valores negativos, vacíos y extremos, carga del modelo, predicción no negativa, cambio de la predicción con las entradas, efecto de la TRM solo con importados, clasificación de riesgo y recomendaciones.
