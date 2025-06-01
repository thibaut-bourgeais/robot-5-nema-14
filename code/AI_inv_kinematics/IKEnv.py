import gymnasium as gym
from gymnasium import spaces
import numpy as np

class IKEnv(gym.Env):
    def __init__(self, robot, max_steps=50):
        super().__init__()
        self.robot = robot
        self.max_steps = max_steps
        self.step_count = 0

        # Espace d'action : 5 angles entre -1 et 1
        self.action_space = spaces.Box(low=-1, high=1, shape=(5,), dtype=np.float32)

        # Espace d'observation : pose cible [x, y, z, r11..r33] = 12D
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(12,), dtype=np.float32)

        self.target_pose = None
        self.current_angles = np.zeros(5)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.step_count = 0
        self.current_angles = np.zeros(5)
        
        # Génère une pose cible en choisissant des angles aléatoires et simulant la pose
        random_angles = np.random.uniform(-np.pi, np.pi, size=5)
        self.robot.set_joint_angles(random_angles)
        pos, R = self.robot.get_end_effector_pose()
        self.target_pose = np.concatenate([pos, R.flatten()])

        return self.target_pose.astype(np.float32), {}

    def step(self, action):
        self.step_count += 1
        self.current_angles = action

        # Appliquer les angles prédits
        self.robot.set_joint_angles(action)
        pred_pos, pred_R = self.robot.get_end_effector_pose()
        pred_pose = np.concatenate([pred_pos, pred_R.flatten()])

        # Calcul de l'erreur sur position + rotation
        error = np.linalg.norm(self.target_pose - pred_pose)

        # Reward = -erreur
        reward = -error
        
        # put [-1;1] angles in [-pi;pi]
        scaled_action = np.pi * action

        # Pénalité si les angles sortent d’un range plausible (optionnel)
        if np.any(scaled_action < -np.pi) or np.any(scaled_action > np.pi):
            reward -= 10.0  # forte pénalité

        terminated = bool(error < 0.01)
        truncated = bool(self.step_count >= self.max_steps)

        info = {"error": error}

        return self.target_pose.astype(np.float32), reward, terminated, truncated, info

    def render(self, mode='human'):
        pass  # tu peux afficher des infos si tu veux
