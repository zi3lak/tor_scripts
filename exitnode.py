from stem.control import Controller
from stem import Flag
from stem.process import launch_tor_with_config
import time

def start_tor():
    # Uruchamiamy Tora z podstawową konfiguracją
    tor_process = launch_tor_with_config(
        config={
            'SocksPort': '9050',         # Port SOCKS dla Tora
            'ControlPort': '9051',       # Port kontrolny
            'ExitNodes': '{us}'          # Opcjonalnie ograniczamy Exit Nodes do kraju, np. USA
        },
        init_msg_handler=lambda line: print(line) if "Bootstrapped" in line else None
    )
    return tor_process

def list_active_exit_nodes():
    # Łączymy się z instancją Tora przez port kontrolny
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  # Standardowo bez hasła

        # Pobieramy informacje o wszystkich aktywnych nodach
        nodes = controller.get_network_statuses()

        exit_nodes = []
        for node in nodes:
            # Sprawdzamy, czy node ma flagę EXIT (oznacza, że jest exit node)
            if Flag.EXIT in node.flags:
                exit_nodes.append({
                    "fingerprint": node.fingerprint,
                    "nickname": node.nickname,
                    "address": node.address,
                    "is_exit": True
                })

        return exit_nodes

if __name__ == "__main__":
    # Uruchamiamy instancję Tora
    tor_process = start_tor()
    
    # Dodajemy opóźnienie, aby Tor miał czas na pełne uruchomienie
    time.sleep(10)  # Możesz dostosować czas, jeśli potrzebujesz więcej lub mniej czasu na inicjalizację

    try:
        exit_nodes = list_active_exit_nodes()

        if exit_nodes:
            print("Lista aktywnych Exit Nodes w sieci Tor:")
            for node in exit_nodes:
                print(f"Nickname: {node['nickname']}, Adres: {node['address']}, Fingerprint: {node['fingerprint']}")
        else:
            print("Nie znaleziono aktywnych Exit Nodes.")
    finally:
        # Zatrzymujemy instancję Tora po zakończeniu działania skryptu
        tor_process.kill()
