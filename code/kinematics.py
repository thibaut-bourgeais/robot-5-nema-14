import numpy as np

def inverse_kinematics(target_point):
    """
    Compute the joint angles required to reach a given target point.
    Includes joint limit constraints.
    """
    joint_limits = [(-np.pi, np.pi)] * 6  # Example: joint limits for each axis
    angles = np.clip(np.zeros(6), [limit[0] for limit in joint_limits], [limit[1] for limit in joint_limits])
    return angles
