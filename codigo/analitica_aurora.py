from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

# 1. Conexión con el clúster
spark = SparkSession.builder \
    .appName("Aurora Analytics - Alejandro") \
    .master("spark://172.31.88.233:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
print("--- Iniciando Análisis de Aurora Tickets ---")

# 2. Truco Maestro: Leer en el Submit y enviar a la RAM de los Workers
with open("aurora_clickstream.jsonl", "r") as f:
    lineas_json = f.readlines()

# Paralelizamos (repartimos) las líneas y las convertimos en DataFrame
rdd = spark.sparkContext.parallelize(lineas_json)
df = spark.read.json(rdd)

# 3. Cálculos
total_eventos = df.count()
print(f"Total de eventos crudos ingeridos: {total_eventos}")

df_limpio = df.filter(col("is_bot_suspicion") == False)
eventos_reales = df_limpio.count()
print(f"Eventos de usuarios reales: {eventos_reales}")
print(f"Bots bloqueados: {total_eventos - eventos_reales}")

# 4. Top 5 Páginas
print("\n--- Top 5 Páginas Más Visitadas ---")
top_paginas = df_limpio.groupBy("url") \
    .agg(count("*").alias("visitas")) \
    .orderBy(col("visitas").desc()) \
    .limit(5)

top_paginas.show()

spark.stop()
print("--- Análisis Completado ---")
