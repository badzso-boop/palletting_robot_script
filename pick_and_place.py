import json
from robodk import robolink, robomath
import math

with open('config.json', 'r') as f:
    config = json.load(f)
RDK = robolink.Robolink(robodk_ip=config['ROBODK_IP'])

items = config['ITEMS']
robot = RDK.Item(items['ROBOT'])
gripper = RDK.Item(items['GRIPPER'])
pickup_frame = RDK.Item(items['BOX_CENTER_PICKUP']) 
box = RDK.Item(items['BOX'])

robot.setSpeed(100)

print("Vissza a Home-hoz...")
robot.MoveJ([0, -90, 90, -90, -90, 0])

robot.setPoseFrame(pickup_frame)
robot.setPoseTool(gripper)

target_orientation = robomath.rotx(math.pi) * robomath.rotz(math.pi / 2)
target_offset = robomath.transl(130, 150, 0)

target_pick = target_offset * robomath.transl(0, 0, 215) * target_orientation
target_pick_approach = target_offset * robomath.transl(0, 0, 250) * target_orientation

try:
    print(f"1. Közelítés: {pickup_frame.Name()}")
    robot.MoveJ(target_pick_approach)
    
    # print("2. Lereszkedés...")
    # robot.MoveL(target_pick)

    # box.setParentStatic(gripper)
    # print(">>> Tárgy rögzítve! <<<")

    # print("3. Visszaemelés...")
    # robot.MoveL(target_pick_approach)

except Exception as e:
    print(f"HIBA: {e}")

print("Program vége.")
