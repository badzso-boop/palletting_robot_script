from robodk import robolink

# 1. Beállítások
# Ide írd a WSL-ből látott Windows IP címet!
WINDOWS_IP = '100.123.35.110'
ROBOT_NAME = 'UR5e'

# 2. Kapcsolódás
RDK = robolink.Robolink(robodk_ip=WINDOWS_IP)

# Ellenőrizzük a kapcsolatot
if not RDK.Connect():
    print("Hiba: Nem sikerült kapcsolódni a RoboDK-hoz!")
    print(f"Ellenőrizd az IP-t ({WINDOWS_IP}) és hogy fut-e a RoboDK a Windowson.")
    exit()

# 3. Robot lekérése
robot = RDK.Item(ROBOT_NAME, robolink.ITEM_TYPE_ROBOT)

if not robot.Valid():
    print(f"Hiba: Nem találom a '{ROBOT_NAME}' nevű robotot a szimulációban!")
    exit()

# 4. Alaphelyzetbe állítás (Home pozíció)
# Ezek a Joint értékek fokban vannak megadva az UR5e-hez
home_joints = [0, -90, 90, -90, -90, 0]

print(f"Robot mozgatása alaphelyzetbe...")
robot.MoveJ(home_joints)

print("Kész! A robot az alaphelyzetben van.")