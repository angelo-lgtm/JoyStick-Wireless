import serial
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
# === Setup Bluetooth serial (change COM3 if needed) ===
ser = serial.Serial('COM4', 38400, timeout=1)
time.sleep(2)  # Allow time for connection
# === Enable interactive mode ===
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Set initial plot limits
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])
ax.set_title("MPU6050 3D Orientation")
# Cube vertices
cube = np.array([
    [-0.5, -0.5, -0.5],
    [ 0.5, -0.5, -0.5],
    [ 0.5,  0.5, -0.5],
    [-0.5,  0.5, -0.5],
    [-0.5, -0.5,  0.5],
    [ 0.5, -0.5,  0.5],
    [ 0.5,  0.5,  0.5],
    [-0.5,  0.5,  0.5]
])
edges = [
    [0,1],[1,2],[2,3],[3,0],
    [4,5],[5,6],[6,7],[7,4],
    [0,4],[1,5],[2,6],[3,7]
]
def rotation_matrix(roll, pitch, yaw):
    r = np.radians(roll)
    p = np.radians(pitch)
    y = np.radians(yaw)
    Rx = np.array([
        [1,0,0],
        [0,np.cos(r),-np.sin(r)],
        [0,np.sin(r), np.cos(r)]
    ])
    Ry = np.array([
        [ np.cos(p),0,np.sin(p)],
        [0,1,0],
        [-np.sin(p),0,np.cos(p)]
    ])
    Rz = np.array([
        [np.cos(y),-np.sin(y),0],
        [np.sin(y), np.cos(y),0],
        [0,0,1]
    ])
    return Rz @ Ry @ Rx
print("Starting live 3D visualization... Move your MPU6050!")
while True:
    try:
        line = ser.readline().decode(errors='ignore').strip()
        if not line:
            continue
        vals = line.split(',')
        if len(vals) != 3:
            continue
        pitch, roll, yaw = map(float, vals)
        R = rotation_matrix(roll, pitch, yaw)
        rotated = cube @ R.T
        ax.cla()
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])
        ax.set_zlim([-1, 1])
        ax.set_title(f"Pitch={pitch:.1f}°  Roll={roll:.1f}°  Yaw={yaw:.1f}°")
        # Draw cube edges
        for e in edges:
            xs = [rotated[e[0]][0], rotated[e[1]][0]]
            ys = [rotated[e[0]][1], rotated[e[1]][1]]
            zs = [rotated[e[0]][2], rotated[e[1]][2]]
            ax.plot(xs, ys, zs, color='royalblue', linewidth=2)
        plt.draw()
        plt.pause(0.01)
    except KeyboardInterrupt:
        print("\nExiting visualization...")
        break
ser.close()
plt.ioff()
plt.show()