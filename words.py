import re
import requests
from stem import Signal
from stem.control import Controller
import time

# Lista stron .onion do przeszukania
onion_sites = [
    # Hidden Wikis
    "http://s4k4ceiapwwgcm3mkb6e4diqecpo7kvdnfr5gg7sph7jjppqkvwwqtyd.onion/",
    "http://6nhmgdpnyoljh5uzr5kwlatx2u3diou4ldeommfxjz3wkhalzgjqxzqd.onion/",
    "http://2jwcnprqbugvyi6ok2h2h7u26qc6j5wxm7feh3znlh2qu3h6hjld4kyd.onion/",
    "http://jgwe5cjqdbyvudjqskaajbfibfewew4pndx52dye7ug3mt3jimmktkid.onion/",
    
    # Bitcoin Anonymity
    "http://y22arit74fqnnc2pbieq3wqqvkfub6gnlegx3cl6thclos4f7ya7rvad.onion/",
    "http://hqfld5smkr4b4xrjcco7zotvoqhuuoehjdvoin755iytmpk4sm7cbwad.onion/",
    "http://mp3fpv6xbrwka4skqliiifoizghfbjy5uyu77wwnfruwub5s4hly2oid.onion/",
    "http://p2qzxkca42e3wccvqgby7jrcbzlf6g7pnkvybnau4szl5ykdydzmvbid.onion/",
    "http://ovai7wvp4yj6jl3wbzihypbq657vpape7lggrlah4pl34utwjrpetwid.onion/",
    
    # Drug Stores
    "http://wbz2lrxhw4dd7h5t2wnoczmcz5snjpym4pr7dzjmah4vi6yywn37bdyd.onion/",
    "http://iwggpyxn6qv3b2twpwtyhi2sfvgnby2albbcotcysd5f7obrlwbdbkyd.onion/",
    "http://rfyb5tlhiqtiavwhikdlvb3fumxgqwtg2naanxtiqibidqlox5vispqd.onion/",
    "http://ajlu6mrc7lwulwakojrgvvtarotvkvxqosb4psxljgobjhureve4kdqd.onion/",
    # More Commercial Links
    "http://prjd5pmbug2cnfs67s3y65ods27vamswdaw2lnwf45ys3pjl55h2gwqd.onion/",
    "http://55niksbd22qqaedkw36qw4cpofmbxdtbwonxam7ov2ga62zqbhgty3yd.onion/",
    "http://s57divisqlcjtsyutxjz2ww77vlbwpxgodtijcsrgsuts4js5hnxkhqd.onion/",
    # Everything Else
    "http://danielas3rtn54uwmofdo3x2bsdifr47huasnmbgqzfrec5ubupvtpid.onion/",
    "http://answerszuvs3gg2l64e6hmnryudl5zgrmwm3vh65hzszdghblddvfiqd.onion/",
    "http://spywaredrcdg5krvjnukp3vbdwiqcv3zwbrcg6qh27kiwecm4qyfphid.onion/",
    # Więcej stron możesz dodać według listy
]

# Słowa kluczowe do wyszukania
search_keywords = ["bitcoin", "privacy", "market"]  # Przykładowe słowa kluczowe

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

# Funkcja do sprawdzania zawartości strony .onion pod kątem słów kluczowych
def search_onion_site(url, keywords):
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
            print(f"Przeszukiwanie strony: {url}")
            content = response.text.lower()
            
            # Szukanie słów kluczowych
            found_keywords = {kw for kw in keywords if kw.lower() in content}
            
            if found_keywords:
                print(f"Znaleziono słowa kluczowe na stronie {url}: {', '.join(found_keywords)}")
            else:
                print(f"Brak słów kluczowych na stronie {url}")
        else:
            print(f"Strona nieaktywna lub wymaga autoryzacji: {url} (Status: {response.status_code})")
    except requests.RequestException as e:
        print(f"Nie udało się połączyć z {url}: {e}")

if __name__ == "__main__":
    # Ustawienie hasła do kontrolnego portu
    control_port_password = "0122"

    for site in onion_sites:
        # Przeszukiwanie strony pod kątem słów kluczowych
        search_onion_site(site, search_keywords)
        
        # Odśwież tożsamość Tor po każdym zapytaniu, aby uniknąć blokad
        renew_tor_ip(password=control_port_password)
        
        # Czekaj 5 sekund, aby uniknąć przeciążenia
        time.sleep(5)
