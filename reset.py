import json
from robodk import robolink, robomath

# 1. Betöltés
with open('config.json', 'r') as f:
    config = json.load(f)
RDK = robolink.Robolink(robodk_ip=config['ROBODK_IP'])

# Tárgyak
items = config['ITEMS']
robot = RDK.Item(items['ROBOT'])
pickup_frame = RDK.Item(items['BOX_CENTER_PICKUP']) 
box = RDK.Item(items['BOX'])

# 1. Doboz leválasztása és visszatétele a helyére
box.setParentStatic(pickup_frame)
box.setPose(robomath.transl(0, 0, 0))

# 2. Robot hazaküldése
robot.MoveJ([0, -90, 90, -90, -90, 0])

print("Állomás visszaállítva!")
