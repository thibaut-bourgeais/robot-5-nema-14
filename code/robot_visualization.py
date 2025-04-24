import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        
        # Timer for live plot
        self.t = 0  # time step
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)  # update every 50 ms

        # Plot exemples
        self.update_plot()
        
    def update_plot(self):
        self.figure.clf()
        ax = self.figure.add_subplot(111, projection='3d')

        # Spirale hélicoïdale
        self.t += 0.1
        theta = np.linspace(0, self.t, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        z = theta

        ax.plot(x, y, z, color='b')
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(0, 10)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        self.canvas.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = RobotWindow()
    window.show()
    sys.exit(app.exec_())