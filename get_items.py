import json
from robodk import robolink

# Konfiguráció betöltése
with open('config.json', 'r') as f:
    config = json.load(f)

RDK = robolink.Robolink(robodk_ip=config['ROBODK_IP'])

if not RDK.Connect():
    print(f"Hiba: Nem sikerült csatlakozni az IP-hez: {config['ROBODK_IP']}")
    exit()

print("\n--- JELENLEGI ELEMEK A ROBODK-BAN ---")
all_items = RDK.ItemList()
for item in all_items:
    print(f"[{item.Type()}] - '{item.Name()}'")

print("\n--- KONFIGURÁCIÓBAN KERESETT ELEMEK ---")
for key, name in config['ITEMS'].items():
    found = RDK.Item(name)
    status = "OK" if found.Valid() else "NEM TALÁLHATÓ!"
    print(f"{key}: '{name}' -> {status}")