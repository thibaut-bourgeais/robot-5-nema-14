import numpy as np
from coordinates import spherical_to_cartesian
from kinematics import inverse_kinematics

def update_robot_state(target_coords):
    """
    Compute new joint angles while considering joint limits.
    """
    target_cartesian = spherical_to_cartesian(*target_coords)
    joint_angles = inverse_kinematics(target_cartesian)
    return joint_angles

if __name__ == "__main__":
    # Example test
    target_coords = (10, np.pi / 4, np.pi / 3)  # r, theta, phi
    angles = update_robot_state(target_coords)
    print("Computed Joint Angles:", angles)
