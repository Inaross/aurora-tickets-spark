# Aurora Tickets - Arquitectura Big Data en AWS

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Apache Spark](https://img.shields.io/badge/apache_spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

## Descripción del Proyecto
**Aurora Tickets** es una plataforma de venta de entradas que se enfrentaba a problemas de conversión, latencia y tráfico anómalo (bots). Este proyecto implementa una solución integral de **Big Data en la nube** para ingestar, procesar y analizar grandes volúmenes de datos transaccionales y de comportamiento web (Clickstream) en tiempo real y en batch.

El proyecto se ha desarrollado siguiendo estrictamente la metodología **CRISP-DM** (Cross-Industry Standard Process for Data Mining).

## Arquitectura de la Solución
La infraestructura ha sido desplegada en **Amazon Web Services (AWS)** bajo un modelo *Pay-as-you-go*, orquestando los siguientes servicios:
* **Cómputo:** Clúster de Apache Spark alojado en instancias **Amazon EC2** (1 Master, 3 Workers, 1 Nodo Submit/Web).
* **Data Lake:** **Amazon S3** organizado en capas (RAW, CURATED y ANALYTICS).
* **Data Warehouse:** **Amazon RDS (MySQL)** para el almacenamiento de KPI de negocio finales.
* **Observabilidad:** **AWS CloudWatch** para la ingesta de logs, análisis con *Logs Insights* y Dashboards interactivos.

## Metodología y Flujo de Datos

### 1. Data Understanding (Generación de Datos)
* **Datos de Negocio:** Generados vía script (`generate_business_data.py`), creando el catálogo, transacciones y campañas en formato CSV.
* **Telemetría Web:** Tráfico masivo simulado (`generador_trafico.py`) contra una API construida en **FastAPI**, generando un log de navegación continuo (`clickstream.jsonl`).

### 2. Data Preparation (Curación en Spark)
* **Job 1 (`job1_curacion.py`):** PySpark extrae los datos de la capa RAW de S3. Realiza limpieza de nulos, filtrado de bots y transforma los datos al formato columnar **Parquet** (particionado por fecha) hacia la capa CURATED.

### 3. Modeling (Procesamiento Analítico)
* **Job 2 (`job2_analitica.py`):** Spark cruza la navegación con los ingresos reales calculando tres modelos clave:
  1. Funnel de conversión diario.
  2. Ranking de interés vs. ingresos por evento.
  3. Detección de anomalías.
* Los resultados masivos se escriben directamente en **Amazon RDS** vía conector JDBC.

### 4. Evaluation & Deployment (Tiempo Real y Visualización)
* Inyección de **>200.000 eventos** locales hacia AWS CloudWatch utilizando **Boto3** (`empujar_logs.py`).
* Ejecución de consultas operativas de seguridad y rendimiento mediante **CloudWatch Logs Insights**.
* Renderizado de las métricas en un **CloudWatch Dashboard** interactivo para consumo directivo.

## 📂 Estructura del Repositorio

```text
📦 aurora-tickets-bigdata
 ┣ 📂 generators/
 ┃ ┣ 📜 generate_business_data.py   # Generador de CSVs transaccionales
 ┃ ┗ 📜 generador_trafico.py        # Simulador de clics contra FastAPI
 ┣ 📂 jobs/
 ┃ ┣ 📜 job1_curacion.py            # Script PySpark: RAW -> CURATED
 ┃ ┗ 📜 job2_analitica.py           # Script PySpark: CURATED -> RDS
 ┣ 📂 observability/
 ┃ ┗ 📜 empujar_logs.py             # Script Boto3: Logs -> CloudWatch
 ┗ 📜 README.md