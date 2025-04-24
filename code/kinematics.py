import numpy as np

class RobotArm:
    def __init__(self):
        # Hardcoded parameters for now
        self.segment_lengths = [5.0, 4.0, 3.0, 2.0]  # Length of each segment
        self.angle_limits = [(-90, 90), (-90, 90), (-90, 90), (-90, 90)]  # Min/max angles in degrees

        self.angles = [0.0 for _ in self.segment_lengths]  # Current angles in degrees

    def set_angles(self, angle_list):
        """Sets angles in degrees, respecting limits."""
        for i, angle in enumerate(angle_list):
            min_angle, max_angle = self.angle_limits[i]
            clamped = max(min(angle, max_angle), min_angle)
            self.angles[i] = clamped

    def get_angles(self):
        """Returns current joint angles in degrees."""
        return self.angles

    def get_joint_positions(self):
        """Computes XYZ positions of each joint using forward kinematics."""
        positions = [(0, 0, 0)]
        current_transform = np.eye(4)

        for angle_deg, length in zip(self.angles, self.segment_lengths):
            theta = np.radians(angle_deg)

            # Rotation around Z
            rot_z = np.array([
                [np.cos(theta), -np.sin(theta), 0, 0],
                [np.sin(theta),  np.cos(theta), 0, 0],
                [0,              0,             1, 0],
                [0,              0,             0, 1],
            ])
            # Translation along X
            trans_x = np.array([
                [1, 0, 0, length],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ])

            current_transform = current_transform @ rot_z @ trans_x
            pos = current_transform[:3, 3]
            positions.append(tuple(pos))

        return positions

    def solve_inverse_kinematics(self, target_pose):
        """
        Given a pose (x, y, z, l, m, n), compute joint angles.
        Not yet implemented — to be solved using iterative IK with cost minimization.
        """
        raise NotImplementedError("IK solver not implemented yet.")
