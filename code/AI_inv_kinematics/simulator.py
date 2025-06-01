import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Link:
    def __init__(self, name, joint_axis, link_vector, parent=None):
        self.name = name
        self.joint_axis = np.array(joint_axis)
        self.link_vector = np.array(link_vector)
        self.joint_angle = 0.0
        self.parent = parent
        self.children = []
        if parent:
            parent.children.append(self)

    def get_local_transform(self):
        # Compute rotation around local axis
        axis = self.joint_axis / np.linalg.norm(self.joint_axis) # Normalize robot axis
        angle = self.joint_angle
        # Anti-symmetric matrix (u x v)
        K = np.array([
            [0, -axis[2], axis[1]],
            [axis[2], 0, -axis[0]],
            [-axis[1], axis[0], 0]
        ])
        # np.eye() = Identity matrix
        # R rodrigues matrix (rotation around axis)
        R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * K @ K
        T = np.eye(4) # Will take R rotation and T translation
        T[:3, :3] = R
        T[:3, 3] = self.link_vector
        return T

    def get_world_transform(self):
        if self.parent:
            return self.parent.get_world_transform() @ self.get_local_transform() # @ = matrix multiplication
        else:
            return self.get_local_transform()

    def get_joint_positions(self):
        # Renvoie la liste des positions (en base monde) de ce lien et de ses enfants
        pos = [self.get_world_transform()[:3, 3]]
        for child in self.children:
            pos.extend(child.get_joint_positions())
        return pos

class Robot:
    def __init__(self):
        self.links = []

    def add_link(self, name, joint_axis, link_vector):
        parent = self.links[-1] if self.links else None
        link: Link = Link(name, joint_axis, link_vector, parent)
        self.links.append(link)

    def set_joint_angles(self, angles):
        assert len(angles) == len(self.links), "Number of angles must match number of joints"
        for link, angle in zip(self.links, angles):
            link.joint_angle = angle

    def get_joint_positions(self):
        if not self.links:
            return []
        return [np.array([0, 0, 0])] + self.links[0].get_joint_positions()
    
    def get_end_effector_pose(self):
        if not self.links:
            return None

        T = self.links[-1].get_world_transform()
        position = T[:3, 3]
        rotation_matrix = T[:3, :3]
        return position, rotation_matrix
    
    def get_link_count(self):
        return len(self.links)

    def summary(self):
        print("Robot structure:")
        for link in self.links:
            print(f"  {link.name}: axis={link.joint_axis}, length={np.linalg.norm(link.link_vector):.2f}, angle={np.degrees(link.joint_angle):.1f}°")
