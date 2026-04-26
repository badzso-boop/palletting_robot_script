import json
from robodk import robolink, robomath
import math

# 1. Betöltés és Kapcsolódás
with open('config.json', 'r') as f:
    config = json.load(f)
RDK = robolink.Robolink(robodk_ip=config['ROBODK_IP'])

# Tárgyak lekérése
items = config['ITEMS']
robot = RDK.Item(items['ROBOT'])
gripper = RDK.Item(items['GRIPPER'])
pickup_frame = RDK.Item(items['BOX_CENTER_PICKUP']) 
box = RDK.Item(items['BOX'])

# Sebesség
robot.setSpeed(100)

# 0. Alaphelyzet
print("Vissza a Home-hoz...")
robot.MoveJ([0, -90, 90, -90, -90, 0])

# 1. FELVÉTEL BEÁLLÍTÁSA
robot.setPoseFrame(pickup_frame)
robot.setPoseTool(gripper)

# --- CÉLPONTOK SZÁMÍTÁSA FINOMHANGOLÁSSAL ---

# 1. Alap orientáció (lefelé néz + 90 fok fordítás balra)
# rotx(pi) -> fejjel lefelé
# rotz(pi/2) -> 90 fokos elforgatás balra (1.5708 radián)
target_orientation = robomath.rotx(math.pi) * robomath.rotz(math.pi / 2)

# 2. Eltolás a megadott értékekkel (X=-30, Y=-127)
target_offset = robomath.transl(130, 150, 0)

# 3. Végleges célpontok összeállítása
target_pick = target_offset * robomath.transl(0, 0, 215) * target_orientation
target_pick_approach = target_offset * robomath.transl(0, 0, 250) * target_orientation

# --- MOZGÁS ---
try:
    print(f"1. Közelítés: {pickup_frame.Name()}")
    robot.MoveJ(target_pick_approach)
    
    # print("2. Lereszkedés...")
    # robot.MoveL(target_pick)

    # # 2. MEGFOGÁS
    # box.setParentStatic(gripper)
    # print(">>> Tárgy rögzítve! <<<")

    # # 3. FELEMELÉS
    # print("3. Visszaemelés...")
    # robot.MoveL(target_pick_approach)

except Exception as e:
    print(f"HIBA: {e}")

print("Program vége.")
