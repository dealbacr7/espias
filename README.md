Proyecto Red de Espías

Archivos:
- comandante.py  -> servidor/master
- espia.py       -> worker genérico parametrizable
- espia_1.py     -> worker rápido
- espia_2.py     -> worker más lento
- espia_vago.py  -> worker especial (extra)
- misiones.py    -> misiones, validación y resolución
- logs.py        -> registro en archivo registro_misiones.txt

Cómo ejecutar:
1) Abre una terminal en esta carpeta y ejecuta:
   python comandante.py

2) En otras dos terminales ejecuta:
   python espia_1.py
   python espia_2.py

Opcional:
   python espia_vago.py

Notas:- El comandante espera por defecto a 2 espías.
- Si quieres usar otros workers, cambia NUM_ESPias_ESPERADOS en comandante.py.
- El comandante espera por defecto a 2 espías.
- Si quieres usar otros workers, cambia NUM_ESPias_ESPERADOS en comandante.py.
