from simulator import Robot
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

robot = Robot()
robot.add_link("root", [0, 0, 1], [0, 0, 0]) # World reference
robot.add_link("base", [0, 1, 0], [0, 0, 10])
robot.add_link("shoulder", [0, 1, 0], [0, 0, 10])
robot.add_link("elbow", [0, 0, 1], [0, 0, 5])
robot.add_link("wrist", [0, 1, 0], [0, 0, 5])
robot.add_link("tool", [0, 0, 1], [0, 0, 0]) # Tool reference

root = tk.Tk()
root.title("Robot Arm Simulator")

fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4)

def update_plot(*args):
    angles_deg = [slider.get() for slider in sliders]
    angles_rad = [np.radians(a) for a in angles_deg]
    robot.set_joint_angles(angles_rad)

    positions = robot.get_joint_positions()
    xs, ys, zs = zip(*positions)

    ax.clear()
    ax.plot(xs, ys, zs, marker='o', linestyle='-', linewidth=2)
    ax.set_xlim(-30, 30)
    ax.set_ylim(-30, 30)
    ax.set_zlim(0, 40)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Robot Arm")
    ax.set_box_aspect([1, 1, 1])
    canvas.draw()

sliders = []
for i in range(robot.get_link_count()):
    slider = tk.Scale(root, from_=-180, to=180, orient='horizontal',
                      label=f"Joint {i+1}", length=200, command=update_plot)
    slider.set(0)
    slider.grid(row=1, column=i, padx=5, pady=5)
    sliders.append(slider)

update_plot()
root.mainloop()