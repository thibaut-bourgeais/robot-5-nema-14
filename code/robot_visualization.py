import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from PyQt5 import QtWidgets, uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class RobotWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("code\GUI.ui", self)

        # Create the fig and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Dynamic layout in the RobotPlot widget
        self.robot_plot_layout = QtWidgets.QVBoxLayout(self.RobotPlot)
        self.robot_plot_layout.setContentsMargins(0, 0, 0, 0)
        self.robot_plot_layout.addWidget(self.canvas)

        # Plot exemples
        self.plot_example()

    def plot_example(self):
        self.figure.clf()  # Clear figure to avoid overlapping plots
        ax = self.figure.add_subplot(111, projection='3d')  # 3D plot

        # Example 3D line
        xs = [0, 1, 2, 3]
        ys = [10, 1, 20, 3]
        zs = [30, 40, 50, 60]
        ax.plot(xs, ys, zs)

        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")
        ax.set_zlabel("Z axis")
        self.canvas.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RobotWindow()
    window.show()
    sys.exit(app.exec_())


class vector:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        """
        Initializes a vector from two points (x1, y1, z1) and (x2, y2, z2).
        """
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
    
    def norm(self):
        """
        Returns the norm (length) of the vector.
        """
        return np.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2 + (self.z2 - self.z1)**2)
    
    def origin(self):
        """
        Returns the origin coordinates of the vector as a tuple (x1, y1, z1)
        """
        return (self.x1, self.y1, self.z1)
    
    def destination(self):
        """
        Returns the destination coordinates of the vector as a tuple (x2, y2, z2)
        """
        return (self.x2, self.y2, self.z2)
    
    def direction(self):
        """
        Returns the direction of the vector as a tuple (dx, dy, dz)
        """
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        dz = self.z2 - self.z1
        return (dx, dy, dz)

    def __str__(self):
        return f"Vector: {self.x1}, {self.y1}, {self.z1} -> {self.x2}, {self.y2}, {self.z2}"