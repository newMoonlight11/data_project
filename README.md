# 🚀 Procesamiento de Archivos con Django y PostgreSQL

Proyecto para procesar archivos de texto plano con formato de ancho fijo, extraer datos estructurados y almacenarlos en una base de datos PostgreSQL. También genera exportaciones en CSV/JSON y expone un endpoint RESTful para automatizar el proceso.

---

## 📌 Características

- ✅ **Procesamiento de archivos**: Extrae datos del archivo `PRUEBA_20250129.txt` usando intervalos definidos.
- 📤 **Exportación**: Genera archivos `output.csv` y `output.json`.
- 🗃️ **Inserción en BD**: Inserta registros en PostgreSQL con validación de campos.
- 🌐 **Endpoint `/parse/`**: Permite enviar el nombre del archivo vía API para procesamiento automático.
  
---

## 📦 Requisitos del Sistema

- Python 3.10+
- Django 5.2
- PostgreSQL 16+
- pandas 2.2.2
- django-environ 0.12.0
- psycopg2-binary 2.9.9
  
---

## 📌 Instrucciones de uso

📤 Genera archivos CSV y JSON
```bash
python manage.py generate_exports PRUEBA_20250129.txt
```
🗃️ Inserta datos en la base de datos
```bash
python manage.py data_prueba PRUEBA_20250129.txt
```

✅ Ejecuta las pruebas
```bash
python manage.py test
```
🌐 Accede al endpoint
```bash
curl -X POST http://127.0.0.1:8000/parse/ \
     -H "Content-Type: application/json" \
     -d '{"filename": "PRUEBA_20250129.txt"}'
```
---
## ✨ Autor
María Camila Villamizar Villamizar
