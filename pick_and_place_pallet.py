import json
import math
import time
from robodk import robolink, robomath
from calc_pallet import calculate_layout

# 1. Betöltés és Kapcsolódás
with open('config.json', 'r') as f:
    config = json.load(f)
RDK = robolink.Robolink(robodk_ip=config['ROBODK_IP'])

# Tárgyak lekérése
items = config['ITEMS']
robot = RDK.Item(items['ROBOT'])
pickup_frame = RDK.Item(items['BOX_CENTER_PICKUP']) 
pallet_frame = RDK.Item(items['PALLET_FRAME'])
gripper = RDK.Item(items['GRIPPER'])
box = RDK.Item(items['BOX'])

# Sebesség és Blending
robot.setSpeed(250)
robot.setRounding(50)

# 2. Raklapozási adatok
nx, ny, points = calculate_layout(40, 48, 12, 10, 10)

# Alap orientáció és eltolás
target_orientation = robomath.rotx(math.pi) * robomath.rotz(math.pi / 2)
target_offset = robomath.transl(130, 150, 0)

# --- BIZTONSÁGI PONTOK ---
conveyor_safety_joints = [-97.034195, -73.137776, 87.715327, -104.577551, -90.000000, -7.034195]
elbow_up_joints = [85.360000, -68.630000, 97.530000, -119.200000, -92.070000, -94.770000]

# --- PROGRAM ---
print(f"=== AUTOMATA PALLETIZÁLÁS INDUL - ROBOT: {robot.Name()} ===")

for i, (px, py) in enumerate(points):
    print(f"\nDoboz {i+1}/{len(points)} | Cél a raklapon: X={px:.1f}, Y={py:.1f}")

    # 1. FELVÉTEL (PICK)
    robot.setRounding(50)
    # Biztonsági tranzit a szalaghoz
    robot.MoveJ(conveyor_safety_joints)
    
    robot.setPoseFrame(pickup_frame)
    robot.setPoseTool(gripper)
    
    target_pick = target_offset * robomath.transl(0, 0, 215) * target_orientation
    target_pick_approach = target_offset * robomath.transl(0, 0, 250) * target_orientation

    robot.MoveJ(target_pick_approach)
    
    robot.setRounding(0)
    robot.MoveL(target_pick)
    
    box.setParentStatic(gripper)
    time.sleep(0.3)
    
    robot.setRounding(50)
    robot.MoveL(target_pick_approach)

    # 2. ÁTMENET A RAKLAPHOZ
    # Vissza a szalag biztonsági pontra, majd át az Elbow Up (raklap) biztonsági pontra
    print("-> Átmenet a biztonsági folyosón...")
    # robot.MoveJ(conveyor_safety_joints)
    robot.MoveJ(elbow_up_joints)

    # 3. LERAKÁS (PLACE)
    robot.setPoseFrame(pallet_frame)
    
    target_place = robomath.transl(px, py, 215) * target_orientation
    target_place_approach = robomath.transl(px, py, 350) * target_orientation

    robot.MoveJ(target_place_approach)
    
    robot.setRounding(0)
    robot.MoveL(target_place)
    
    box.setParentStatic(pallet_frame)
    time.sleep(0.3)
    
    robot.setRounding(50)
    robot.MoveL(target_place_approach)
    
    # 4. VISSZATÉRÉS ELŐKÉSZÍTÉSE
    # Lerakás után vissza az Elbow Up pontra
    # robot.MoveJ(elbow_up_joints)
    
    # RESET a szimulációhoz (hogy a következő dobozt is fel tudjuk venni)
    box.setParentStatic(pickup_frame)
    box.setPose(robomath.transl(0,0,0))

print("\nPalletizálás sikeresen befejezve.")
robot.MoveJ(elbow_up_joints)
