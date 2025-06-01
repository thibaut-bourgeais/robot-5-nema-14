import numpy as np
import pandas as pd
from simulator import Robot

# Initialize robot
robot = Robot()
robot.add_link("root", [0, 0, 1], [0, 0, 0]) # World reference
robot.add_link("base", [0, 1, 0], [0, 0, 10])
robot.add_link("shoulder", [0, 1, 0], [0, 0, 10])
robot.add_link("elbow", [0, 0, 1], [0, 0, 5])
robot.add_link("wrist", [0, 1, 0], [0, 0, 5])
# robot.add_link("tool", [0, 0, 1], [0, 0, 0]) # Tool reference

# Generate dataset
n_samples = 10000
angle_limits = np.radians([-180, 180])

X = []
Y = []


for _ in range(n_samples):
    input_angles = np.random.uniform(*angle_limits, size=5)
    robot.set_joint_angles(input_angles)
    input_pos, input_R = robot.get_end_effector_pose()    
    row = np.concatenate([input_angles, input_pos, input_R.flatten()])
    X.append(row)
    
    output_angles = np.random.uniform(*angle_limits, size=5)
    robot.set_joint_angles(output_angles)
    output_pos, output_R = robot.get_end_effector_pose()
    output_vec = np.concatenate([output_pos, output_R.flatten()])
    Y.append(output_vec)

# Save
df = pd.DataFrame(np.hstack([X, Y]), columns=[
    'theta1_i', 'theta2_i', 'theta3_i', 'theta4_i', 'theta5_i',
    'x_i', 'y_i', 'z_i',
    'r11_i', 'r12_i', 'r13_i',
    'r21_i', 'r22_i', 'r23_i',
    'r31_i', 'r32_i', 'r33_i',
    
    'x_o', 'y_o', 'z_o',
    'r11_o', 'r12_o', 'r13_o',
    'r21_o', 'r22_o', 'r23_o',
    'r31_o', 'r32_o', 'r33_o'
])

print(df.head())          # Preview in terminal
df.to_csv("robot_dataset.csv", index=False)