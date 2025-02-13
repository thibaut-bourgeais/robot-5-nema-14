import numpy as np

def spherical_to_cartesian(r, theta, phi):
    """
    Convert spherical coordinates (r, theta, phi) to Cartesian (x, y, z).
    Theta: azimuthal angle (in radians)
    Phi: polar angle (in radians)
    """
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    return np.array([x, y, z])
