# Capturas de evidencia

Capturas de página completa (1440 px de ancho) tomadas el 2026-11-09 con la app ejecutándose localmente.

| Archivo | Escenario | URL para reproducir |
|---|---|---|
| `capturas/escenario_0.png` | Escenario base | `http://localhost:8501/?escenario=0` |
| `capturas/escenario_1.png` | Prueba 1: favorable | `http://localhost:8501/?escenario=1` |
| `capturas/escenario_2.png` | Prueba 2: presión de costos | `http://localhost:8501/?escenario=2` |
| `capturas/escenario_3.png` | Prueba 3: crítico | `http://localhost:8501/?escenario=3` |

Para regenerarlas, con la app en ejecución (macOS, Chrome):

```bash
for i in 0 1 2 3; do "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --hide-scrollbars --window-size=1440,2750 --virtual-time-budget=40000 \
  --screenshot=docs/capturas/escenario_$i.png "http://localhost:8501/?escenario=$i"; done
```

Si una imagen sale en blanco (la app aún cargaba), repita el comando. Después de publicar la app, se recomienda tomar también capturas desde la URL pública.
