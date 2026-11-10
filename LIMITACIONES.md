# Limitaciones — CaféNexo IA

## Del modelo de IA
- Es un modelo **académico y orientativo**: produce una *estimación académica orientativa*, no una predicción empresarial exacta.
- Se entrenó con **datos simulados**, no con ventas reales de una cafetería.
- Una buena métrica (R² 0,98) sobre datos simulados **no demuestra** desempeño comercial real: el modelo solo recupera la estructura con la que se generaron los datos.
- No incluye competencia, clima, ubicación, calidad del producto, eventos, día de la semana ni preferencias del consumidor.
- Fuera de los rangos de entrenamiento no es confiable. Por eso la app bloquea valores fuera de rango.
- La relación aprendida es casi lineal. En la realidad la demanda puede tener umbrales o saturación.

## De los cálculos económicos
- Modelo mensual estático: no incluye impuestos, depreciación, financiación, capital de trabajo ni estacionalidad dentro del mes.
- La inversión en promoción solo actúa como variable de demanda. Se asume **incluida en los costos fijos mensuales**: no se suma por separado, para respetar las fórmulas acordadas con el Excel.
- La inflación entra como variable explicativa de la demanda. No reajusta automáticamente precios ni costos.
- La TRM solo afecta la estimación cuando se activa «Usa insumos importados».
- El precio de máxima utilidad que muestra el gráfico de sensibilidad es una referencia, no un precio óptimo garantizado.

## De la decisión
- El riesgo y la recomendación son reglas económicas declaradas, no una segunda IA.
- La herramienta **no garantiza rentabilidad** y no reemplaza la validación del administrador ni la asesoría profesional.

## Seguridad y privacidad
- No solicita ni almacena datos personales. No guarda las entradas del usuario.
- No usa APIs externas ni claves. Funciona sin servicios pagos.
