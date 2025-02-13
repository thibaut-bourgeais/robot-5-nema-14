import pybullet as p
import pybullet_data
import time

# Connexion PyBullet
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Charger le plan
planeId = p.loadURDF("plane.urdf")

# Charger ton robot 6 axes
robotId = p.loadURDF("code/six_axis_robot.urdf", basePosition=[0, 0, 0])

# Récupérer le nombre de joints
num_joints = p.getNumJoints(robotId)
print(f"Nombre d'articulations: {num_joints}")

# Boucle de simulation
while True:
    for i in range(num_joints):
        p.setJointMotorControl2(robotId, i, p.POSITION_CONTROL, targetPosition=0.5)
    p.stepSimulation()
    time.sleep(0.05)
