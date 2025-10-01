# Caso-1---Merkadit---Daniel-Zumbado-y-Steven-Feng
# Merkadit API

API REST para la gestión de negocios, productos y ventas de Merkadit.  
Implementada con **FastAPI** y **MySQL** usando **stored procedures** para registrar ventas y liquidar comercios.

---

## Requisitos de instalacion previo

- Python 3.11+
- Docker y Docker Compose
- MySQL 8.x
- Postman (opcional para pruebas)

---

## Instalación

1. **Clonar el repositorio**

```bash
git clone <URL_DEL_REPOSITORIO>
cd merkaditApi

creacion_de_un_contenedor

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "tu_contraseña"
MYSQL_DB = "merkadit_db"
MYSQL_CHARSET = "utf8mb4"

comando_para_correr_el_contenedor
docker run --name merkadit-mysql -e MYSQL_ROOT_PASSWORD=tu_contraseña -p 3306:3306 -d mysql:8

comando_para_conectarnos_al_contenedor_que_levantamos

docker exec -it merkadit-mysql bash
mysql -u root -p

creacion_del_database
CREATE DATABASE IF NOT EXISTS merkadit_db;
USE merkadit_db;

Y_para_crear_las_tablas_del_model_nos_dirigimos_en_terminal_a_la_carpeta_merkadit_con_el_comando_cd_y_ejecutamos_Python-createTables.py
de_esta_manera,se_crean_todas_las_tablas_en_su_base_de_datos

Para_realizar_los_inserts,es_solo_copiar_y_pegar_el_seed_en_el_terminal_al_igual
que_el_view

para_ejecutar_los_scripts_de_tablas_y_los_stores_procedures
SOURCE /ruta/a/tus/scripts/schema.sql;
SOURCE /ruta/a/tus/scripts/stored_procedures.sql;

comando_para_levantar_el_api
uvicorn main:app --reload

y_link_para_probar_el_api_y_tendria_un_cuerpo_JSON
http://127.0.0.1:8000/docs

{
  "productoName": "Producto A",
  "comercioName": "Comercio X",
  "cantidad": 2,
  "monto_pagado": 100,
  "medio_pago_name": "Tarjeta",
  "confirmaciones_pago": ["CONF12345"],
  "numeros_referencia": ["REF6789"],
  "numero_factura": 101,
  "cliente": "Juan Pérez",
  "descuentos_aplic": {"porcentaje": 10}
}

