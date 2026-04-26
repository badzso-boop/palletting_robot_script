import json
import math
import time
from robodk import robolink, robomath
from calc_pallet import calculate_layout

with open('config.json', 'r') as f:
    config = json.load(f)
RDK = robolink.Robolink(robodk_ip=config['ROBODK_IP'])

items = config['ITEMS']
robot = RDK.Item(items['ROBOT'])
conveyor = RDK.Item(items['CONVEYOR'])
pickup_frame = RDK.Item(items['BOX_CENTER_PICKUP']) 
pallet_frame = RDK.Item(items['PALLET_FRAME'])
gripper = RDK.Item(items['GRIPPER'])

robot.setSpeed(300)
robot.setRounding(50)

nx, ny, points = calculate_layout(48, 48, 12, 10, 40)

target_orientation = robomath.rotx(math.pi) * robomath.rotz(math.pi / 2)
target_offset = robomath.transl(130, 150, 0)

conveyor_safety_joints = [-97.034195, -73.137776, 87.715327, -104.577551, -90.000000, -7.034195]
elbow_up_joints = [73.620629, -77.973517, 94.115421, -106.141905, -90.000000, -106.379371]

print(f"=== AUTOMATA SOROZAT-PALLETIZÁLÁS INDUL ===")

conveyor.setJoints([0])

for i, (px, py) in enumerate(points):
    box_name = f"{items['BOX_PREFIX']}{i+1}"
    current_box = RDK.Item(box_name)
    
    if not current_box.Valid():
        print(f"HIBA: Nem találom a dobozt: {box_name}")
        continue

    print(f"\n>>> [{i+1}/12] {box_name} mozgatása ide: X={px:.1f}, Y={py:.1f}")

    conv_pos = i * -300
    print(f"Szalag pozíció: {conv_pos} mm")
    conveyor.setJoints([conv_pos])
    time.sleep(0.2)

    robot.setRounding(50)
    robot.MoveJ(conveyor_safety_joints)
    
    robot.setPoseFrame(pickup_frame)
    robot.setPoseTool(gripper)
    
    target_pick = target_offset * robomath.transl(0, 0, 215) * target_orientation
    target_pick_approach = target_offset * robomath.transl(0, 0, 250) * target_orientation

    robot.MoveJ(target_pick_approach)
    
    robot.setRounding(0)
    robot.MoveL(target_pick)
    
    current_box.setParentStatic(gripper)
    time.sleep(0.3)
    
    robot.setRounding(50)
    robot.MoveL(target_pick_approach)

    robot.MoveJ(elbow_up_joints)

    robot.setPoseFrame(pallet_frame)
    
    target_place = robomath.transl(px, py, 215) * target_orientation
    target_place_approach = robomath.transl(px, py, 450) * target_orientation

    robot.MoveJ(target_place_approach)
    
    robot.setRounding(0)
    robot.MoveL(target_place)
    
    current_box.setParentStatic(pallet_frame)
    time.sleep(0.3)
    
    robot.setRounding(50)

print("\nKész! A raklap megtelt.")
robot.MoveJ(elbow_up_joints)
