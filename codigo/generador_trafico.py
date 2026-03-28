import requests
import random
import time
import json
import concurrent.futures
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
URL_WEB = "http://<PON_AQUI_LA_IP_PUBLICA_DE_TU_WEB>/track"
TOTAL_EVENTOS = 205000
HILOS = 10  # Trabajadores simultáneos para ir rápido

# Catálogos de simulación
TIPOS_EVENTO = ["page_view", "click", "add_to_cart", "purchase", "logout"]
PAGINAS = ["/home", "/conciertos", "/festivales", "/teatro", "/pago", "/perfil"]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)",
    "Bot-Malicioso-Scraper-v1.0"
]

def generar_evento(id_evento):
    # Simular 7 días de datos hacia atrás
    dias_restar = random.uniform(0, 7)
    fecha_simulada = datetime.now() - timedelta(days=dias_restar)
    
    # Lógica de "Bots" (1% de los eventos hacen cosas raras)
    es_bot = random.random() < 0.01
    
    payload = {
        "event_id": f"evt_{id_evento}",
        "user_id": random.randint(1, 5000) if not es_bot else 999999,
        "session_id": f"sess_{random.randint(1, 10000)}",
        "event_type": random.choices(TIPOS_EVENTO, weights=[50, 20, 15, 10, 5])[0],
        "url": random.choice(PAGINAS),
        "user_agent": random.choice(USER_AGENTS) if not es_bot else "Bot-Malicioso-Scraper-v1.0",
        "client_timestamp": int(fecha_simulada.timestamp()),
        "is_bot_suspicion": es_bot
    }
    
    try:
        requests.post(URL_WEB, json=payload, timeout=5)
    except:
        pass # Ignoramos fallos puntuales de red para no detener el ataque

print(f"Iniciando bombardeo de {TOTAL_EVENTOS} eventos hacia {URL_WEB}...")
tiempo_inicio = time.time()

# Usar multihilo para enviar miles de peticiones por minuto
with concurrent.futures.ThreadPoolExecutor(max_workers=HILOS) as executor:
    executor.map(generar_evento, range(TOTAL_EVENTOS))

tiempo_fin = time.time()
print(f"¡Bombardeo completado en {round((tiempo_fin - tiempo_inicio)/60, 2)} minutos!")