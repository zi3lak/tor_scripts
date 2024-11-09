from stem import Signal, CircStatus
from stem.control import Controller

# Funkcja monitorująca maksymalnie wiele zdarzeń Tor
def monitor_tor_events(password="0122"):
    with Controller.from_port(port=9051) as controller:
        # Autoryzacja za pomocą hasła
        controller.authenticate(password=password)

        # Lista wszystkich typów zdarzeń do monitorowania
        event_types = [
            "NOTICE",    # Informacje systemowe
            "WARN",      # Ostrzeżenia
            "ERR",       # Błędy
            "CIRC",      # Tworzenie i zamykanie obwodów
            "STREAM",    # Ruch w obwodach
            "ORCONN",    # Połączenia pomiędzy przekaźnikami
            "BW",        # Wykorzystanie pasma
            "ADDRMAP",   # Mapowanie adresów (np. DNS)
            "NS",        # Zmiany w stanie przekaźników
            "STATUS_CLIENT",   # Status klienta
            "STATUS_SERVER",   # Status serwera
            "GUARD",     # Zdarzenia dotyczące przekaźników Guard
            "DESCCHANGED", # Zmiana deskryptora przekaźnika
            "STATUS_GENERAL" # Ogólne statusy
        ]

        # Subskrypcja wszystkich typów zdarzeń
        for event_type in event_types:
            controller.add_event_listener(lambda event: print(event), event_type)

        print("Nasłuchiwanie maksymalnie wielu zdarzeń Tora (ControlPort 9051)...")

        # Informacje o aktualnych obwodach
        for circ in controller.get_circuits():
            if circ.status == CircStatus.BUILT:
                print(f"Obwód {circ.id} utworzony:")
                for relay in circ.path:
                    # relay[0] to fingerprint lub nickname, relay[1] to fingerprint
                    print(f" - {relay[0]} ({relay[1]})")

        input("Naciśnij Enter, aby zakończyć nasłuchiwanie.\n")

# Uruchomienie monitorowania
monitor_tor_events()
