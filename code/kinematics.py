import numpy as np

def rotation_matrix(axis, angle_rad):
    """Returns the rotation matrix around a given axis ('x', 'y', or 'z') by angle_rad."""
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    if axis == 'x':
        return np.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1],
        ])
    elif axis == 'y':
        return np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1],
        ])
    elif axis == 'z':
        return np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])
    else:
        raise ValueError(f"Invalid axis {axis}. Must be 'x', 'y' or 'z'.")

def translation_along_x(length):
    """Returns a homogeneous transformation matrix for translation along X."""
    return np.array([
        [1, 0, 0, length],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

class RobotArm:
    def __init__(self):
        # Hardcoded joints for now
        self.joints = [
            Joint(axis='z', length=5.0, min_angle=-180, max_angle=180),
            Joint(axis='y', length=4.0, min_angle=-90, max_angle=90),
            Joint(axis='y', length=3.0, min_angle=-90, max_angle=90),
            Joint(axis='x', length=2.0, min_angle=-90, max_angle=90),
        ]
    def set_angles(self, angle_list):
        """Sets angles in degrees, respecting limits."""
        for joint, angle in zip(self.joints, angle_list):
            clamped = max(min(angle, joint.max_angle), joint.min_angle)
            joint.angle = clamped

    def get_angles(self):
        """Returns list of current angles (degrees)."""
        return [joint.angle for joint in self.joints]

    def get_joint_positions(self):
        """Returns the 3D positions of all joints."""
        positions = [(0, 0, 0)]
        T = np.eye(4)

        for joint in self.joints:
            # Rotation around axis
            theta_rad = np.radians(joint.angle)
            R = rotation_matrix(joint.axis, theta_rad)

            # Translation along X
            T = T @ R @ translation_along_x(joint.length)

            pos = T[:3, 3]
            positions.append(tuple(pos))

        return positions

    def _compute_forward_kinematics_from(self, angles):
        """Returns the 3D joint positions from a specific list of angles."""
        positions = [(0, 0, 0)]
        T = np.eye(4)

        for joint, angle in zip(self.joints, angles):
            theta_rad = np.radians(angle)
            R = rotation_matrix(joint.axis, theta_rad)
            T = T @ R @ translation_along_x(joint.length)
            pos = T[:3, 3]
            positions.append(tuple(pos))

        return positions
    
    def solve_inverse_kinematic_position(self, target_xyz, max_iterations=100, tolerance=1e-2):
        """
        Applies CCD algorithm to move the end-effector to target_xyz (only position).
        Returns the list of solution angles in degrees.
        """
        angles = self.get_angles()  # Start from current configuration
        segment_count = len(self.joints)

        for iteration in range(max_iterations):
            
            # Compute positions from current angles
            joint_positions = self._compute_forward_kinematics_from(angles)

            end_effector = np.array(joint_positions[-1])
            target = np.array(target_xyz)

            # Check convergence
            if np.linalg.norm(end_effector - target) < tolerance:
                break

            # Loop joints from end to base
            for i in reversed(range(segment_count)):
                joint_pos = np.array(joint_positions[i])
                current_end = np.array(joint_positions[-1])

                vec_current = (current_end - joint_pos).astype(np.float64)
                vec_target = (target - joint_pos).astype(np.float64)


                norm_current = np.linalg.norm(vec_current)
                norm_target = np.linalg.norm(vec_target)
                if norm_current < 1e-6 or norm_target < 1e-6:
                    continue

                vec_current /= norm_current
                vec_target /= norm_target

                # Compute rotation axis
                axis = self.joints[i].axis.lower()

                # Find rotation needed
                if axis == 'x':
                    proj_current = np.array([0, vec_current[1], vec_current[2]])
                    proj_target = np.array([0, vec_target[1], vec_target[2]])
                elif axis == 'y':
                    proj_current = np.array([vec_current[0], 0, vec_current[2]])
                    proj_target = np.array([vec_target[0], 0, vec_target[2]])
                elif axis == 'z':
                    proj_current = np.array([vec_current[0], vec_current[1], 0])
                    proj_target = np.array([vec_target[0], vec_target[1], 0])
                else:
                    raise ValueError(f"Invalid joint axis '{axis}'.")

                norm_proj_current = np.linalg.norm(proj_current)
                norm_proj_target = np.linalg.norm(proj_target)
                if norm_proj_current < 1e-6 or norm_proj_target < 1e-6:
                    continue

                proj_current /= norm_proj_current
                proj_target /= norm_proj_target

                # Compute angle between projections
                dot = np.clip(np.dot(proj_current, proj_target), -1.0, 1.0)
                delta_angle_rad = np.arccos(dot)

                cross = np.cross(proj_current, proj_target)
                direction = np.sign(cross[np.argmax(np.abs(cross))])

                delta_angle_deg = np.degrees(delta_angle_rad * direction)

                # Apply rotation
                angles[i] += delta_angle_deg

                # Clamp within joint limits
                angles[i] = max(min(angles[i], self.joints[i].max_angle), self.joints[i].min_angle)

        return angles

class Joint:
    def __init__(self, axis='z', length=1.0, min_angle=0, max_angle=360):
        self.axis = axis  # 'x', 'y', or 'z'
        self.length = length
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.angle = 0.0
