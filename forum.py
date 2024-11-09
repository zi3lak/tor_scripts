import re
import requests
from stem import Signal
from stem.control import Controller
import time

# Lista stron .onion do sprawdzenia
onion_sites = [
    "http://libraryfyuybp7oyidyya3ah5xvwgyx6weauoini7zyz555litmmumad.onion",  # Przykładowy adres
    "http://s4k4ceiapwwgcm3mkb6e4diqecpo7kvdnfr5gg7sph7jjppqkvwwqtyd.onion",
    "http://wbz2lrxhw4dd7h5t2wnoczmcz5snjpym4pr7dzjmah4vi6yywn37bdyd.onion/",
]

# Funkcja odświeżająca tożsamość Tor, zmieniająca IP
def renew_tor_ip(password=None):
    try:
        with Controller.from_port(port=9051) as controller:
            # Uwierzytelnianie z hasłem
            controller.authenticate(password=password)
            
            # Wysłanie sygnału do zmiany tożsamości (zmiana IP)
            controller.signal(Signal.NEWNYM)
            print("Zmieniono adres IP Tora")
    except Exception as e:
        print(f"Błąd podczas odświeżania IP Tora: {e}")

# Funkcja sprawdzająca dostępność strony .onion
def check_onion_site(url):
    try:
        # Konfiguracja proxy Tor
        session = requests.Session()
        session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        
        # Pobieranie zawartości strony
        response = session.get(url, timeout=10)
        
        # Sprawdzanie odpowiedzi HTTP
        if response.status_code == 200:
            print(f"Strona dostępna: {url}")
        else:
            print(f"Strona nieaktywna lub wymaga autoryzacji: {url} (Status: {response.status_code})")
    except requests.RequestException as e:
        print(f"Nie udało się połączyć z {url}: {e}")

if __name__ == "__main__":
    # Ustawienie hasła do kontrolnego portu
    control_port_password = "0122"

    for site in onion_sites:
        print(f"Sprawdzanie strony: {site}")
        check_onion_site(site)
        
        # Odśwież tożsamość Tor
        renew_tor_ip(password=control_port_password)
        
        # Czekaj 5 sekund, aby uniknąć przeciążenia
        time.sleep(5)
