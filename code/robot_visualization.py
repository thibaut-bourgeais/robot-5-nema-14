import pybullet as p
import pybullet_data
import time
import numpy as np
from robot_state import update_robot_state

class Robot3DSimulator:
    def __init__(self):
        # Initialisation de PyBullet
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)

        # Chargement du plan de référence
        self.planeId = p.loadURDF("plane.urdf")

        # Chargement du robot KUKA 6 axes
        self.robotId = p.loadURDF("kuka_iiwa/model.urdf", basePosition=[0, 0, 0])

        # Nombre de joints du robot
        self.num_joints = p.getNumJoints(self.robotId)

        # Définition des limites articulaires (exemple)
        self.joint_limits = [(-np.pi, np.pi)] * self.num_joints

    def set_joint_positions(self, angles):
        """
        Met à jour les angles des joints du robot dans la simulation.
        """
        for i, angle in enumerate(angles):
            clamped_angle = np.clip(angle, self.joint_limits[i][0], self.joint_limits[i][1])
            p.setJointMotorControl2(self.robotId, i, p.POSITION_CONTROL, targetPosition=clamped_angle)
            print(f"Joint {i}: targetPosition = {clamped_angle:.2f}")  # Debug

    def generate_random_target(self):
        """
        Génère une position aléatoire en coordonnées sphériques :
        - Distance r entre 5 et 15
        - Angle theta entre 0 et 2π
        - Angle phi entre 0 et π/2 (pour rester au-dessus du plan)
        """
        r = np.random.uniform(5, 15)
        theta = np.random.uniform(0, 2 * np.pi)
        phi = np.random.uniform(0, np.pi / 2)
        print(f"Nouvelle position cible: r={r:.2f}, theta={theta:.2f}, phi={phi:.2f}")  # Debug
        return (r, theta, phi)

    def update(self):
        """
        Génère une position aléatoire et met à jour la simulation.
        """
        target_coords = self.generate_random_target()
        angles = update_robot_state(target_coords)

        # Vérification des angles obtenus
        print("Angles calculés :", angles)

        self.set_joint_positions(angles)

    def run(self):
        """
        Boucle principale d'animation.
        Génère une nouvelle position toutes les 2 secondes.
        """
        while True:
            self.update()
            for _ in range(40):  # Attendre 2 secondes en simulant 40 steps (50ms chaque)
                p.stepSimulation()
                time.sleep(0.05)

if __name__ == "__main__":
    simulator = Robot3DSimulator()
    simulator.run()
