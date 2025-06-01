import time
import torch
from simulator import Robot
from IKEnv import IKEnv
import os

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

robot = Robot()
robot.add_link("root", [0, 0, 1], [0, 0, 0]) # World reference
robot.add_link("base", [0, 1, 0], [0, 0, 10])
robot.add_link("shoulder", [0, 1, 0], [0, 0, 10])
robot.add_link("elbow", [0, 0, 1], [0, 0, 5])
robot.add_link("wrist", [0, 1, 0], [0, 0, 5])


MODEL_DIR = "./ppo_iknet_best/"
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.zip")

env = Monitor(IKEnv(robot))
check_env(env) # Check if the env is properly set

eval_env = Monitor(IKEnv(robot))

# Evaluation callback (save the best model)
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path="./ppo_iknet_best/",
    log_path="./ppo_iknet_logs/",
    eval_freq=5000,
    deterministic=True,
    render=False
)

policy_kwargs = dict(
    net_arch=[64, 128, 64],  # 3 layers
    activation_fn=torch.nn.ReLU
)

# Model found, continue training
if os.path.isfile(MODEL_PATH):
    print("Model found, continuing training...")
    model = PPO.load(MODEL_PATH, env=env)
    # Don't put the timer back to zero
    model.learn(total_timesteps=300_000, callback=eval_callback, reset_num_timesteps=False)
else:
    print("No model found, training from zero...")
    model = PPO(
    "MlpPolicy",
    env,
    policy_kwargs=policy_kwargs,
    verbose=1,
    tensorboard_log="./ppo_iknet_tensorboard/",
    device="cpu"
    )
    model.learn(total_timesteps=300_000, callback=eval_callback)

if 0:
    obs, _ = env.reset()

    start = time.time()
    num_of_steps = 1000
    for _ in range(num_of_steps):
        action, _ = model.predict(obs, deterministic=True)
    end = time.time()

    print(f"Inference time per step: {(end - start) / num_of_steps:.6f} sec")
