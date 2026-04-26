import json
from robodk import robolink, robomath

# 1. Betöltés és Kapcsolódás
with open('config.json', 'r') as f:
    config = json.load(f)
RDK = robolink.Robolink(robodk_ip=config['ROBODK_IP'])

# Tárgyak lekérése
items = config['ITEMS']
robot = RDK.Item(items['ROBOT'])
conveyor = RDK.Item(items['CONVEYOR'])
box_prefix = items['BOX_PREFIX']
original_parent = RDK.Item('Frame 5')

if not original_parent.Valid():
    original_parent = conveyor

# 1. Robot alaphelyzetbe
print("Robot hazaküldése...")
home_joints = [85.36, -68.63, 97.53, -119.20, -92.07, -94.77]
robot.setJoints(home_joints)

# 2. Szalag alaphelyzetbe
print("Szalag visszaállítása...")
conveyor.setJoints([0])

# 3. Dobozok visszaállítása a megadott eltolással
print("Dobozok sorba rendezése a szalagon...")
for i in range(1, 13):
    box_name = f"{box_prefix}{i}"
    box = RDK.Item(box_name)
    
    if box.Valid():
        # Visszatesszük a Frame 5 alá
        box.setParentStatic(original_parent)
        
        # Kiszámoljuk az eltolást:
        # X: 0, 300, 600, 900...
        # Y: 150 (fix)
        pos_x = (i - 1) * 300
        pos_y = 150
        
        box.setPose(robomath.transl(pos_x, pos_y, 0))

print("Állomás visszaállítva, dobozok sorban (Y=150, X step=300).")
