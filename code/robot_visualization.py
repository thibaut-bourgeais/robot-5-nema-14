import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from kinematics import RobotArm 

class RobotWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("code/GUI.ui", self)

        # Create the fig and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Dynamic layout in the RobotPlot widget
        self.robot_plot_layout = QtWidgets.QVBoxLayout(self.RobotPlot)
        self.robot_plot_layout.setContentsMargins(0, 0, 0, 0)
        self.robot_plot_layout.addWidget(self.canvas)
        
        self.arm = RobotArm()
        self.start_angles = self.arm.get_angles()
        self.target_angles = self.arm.solve_inverse_kinematic_position((7, 2, 5))

        self.steps_total = 100  # For 5s at 50ms/tick
        self.current_step = 0
        
        # Timer for live plot
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)  # update every 50 ms

        self.update_plot()
        
    def interpolate_angles(self, alpha):
        """Interpolation linéaire entre angles de départ et cible."""
        return [
            (1 - alpha) * a + alpha * b
            for a, b in zip(self.start_angles, self.target_angles)
        ]

    def update_plot(self):
        self.figure.clf()
        ax = self.figure.add_subplot(111, projection='3d')

        # Interpolation sur angles
        alpha = min(1.0, self.current_step / self.steps_total)
        interpolated = self.interpolate_angles(alpha)
        self.arm.set_angles(interpolated)
        positions = self.arm.get_joint_positions()

        # Tracé des segments
        xs, ys, zs = zip(*positions)
        ax.plot(xs, ys, zs, marker='o', color='darkorange')

        # Axes fixes pour la visualisation
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_zlim(0, 10)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        self.canvas.draw()
        self.current_step += 1


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RobotWindow()
    window.show()
    sys.exit(app.exec_())