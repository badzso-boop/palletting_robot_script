import json
from robodk import robolink

# 1. Betöltés
with open('config.json', 'r') as f:
    config = json.load(f)
RDK = robolink.Robolink(robodk_ip=config['ROBODK_IP'])

if not RDK.Connect():
    print(f"Hiba: Nem sikerült csatlakozni: {config['ROBODK_IP']}")
    exit()

all_items = RDK.ItemList()

print("\n--- ROBODK ÁLLOMÁS RÉSZLETES ADATAI ---")
print("Név | Típus | Szülő | Pozíció [X, Y, Z, rx, ry, rz]")
print("-" * 60)

for item in all_items:
    name = item.Name()
    type_id = item.Type()
    parent = item.Parent()
    parent_name = parent.Name() if parent.Valid() else "Station"
    
    # Pozíció lekérése listaként [X, Y, Z, rx, ry, rz]
    # A Pose() a szülőhöz képesti helyzetet adja meg
    pose_list = item.Pose().tolist()
    
    print(f"['{name}'] | Típus: {type_id} | Szülő: '{parent_name}'")
    print(f"  Pose: {pose_list}")

print("-" * 60)
