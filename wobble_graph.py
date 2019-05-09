import sqlite3
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation
plt.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'

class WobbleGraph:
    wobble_data = []
    ax = None

    def __init__(self, high_def=False):
        self.set_data()
        self.max_count = max([wobble_point.get('count') for wobble_point in self.wobble_data])

        self.fig = plt.figure()
        self.set_axis()
        anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.plot_data, frames=360, interval=10, blit=False)
        if high_def:
            self.fig.set_size_inches(19.2, 12, True)
            dpi = 300
        else:
            dpi = 72
        anim.save('index.mp4', bitrate=102400, dpi=dpi, fps=25)

    def set_data(self):
        #   Get from database
        conn = sqlite3.connect('sensordata.db')
        cursor = conn.cursor()
        cursor.execute("SELECT x, y, z FROM wobble_readings")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        #   Flatten
        flattened_map = {}
        for result in results:
            x = int(result[0])
            y = int(result[1])
            z = int(result[2])

            key = "%s_%s_%s" % (x, y, z)

            if key not in flattened_map:
                flattened_map[key] = {"x": x, "y": y, "z": z, "count": 1}
            else:
                flattened_map[key]['count'] += 1
        self.wobble_data = [value for key, value in flattened_map.items()]

        #   Scale Data
        max_count = max([wobble_point.get('count') for wobble_point in self.wobble_data])

        for wobble_point in self.wobble_data:
            wobble_point['scaled'] = (float(wobble_point.get('count')) / max_count)

    def set_axis(self):
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.ax.grid(False)

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])

        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = True

        self.ax.w_xaxis.line.set_color((0.0, 0.0, 0.0, 0.0))
        self.ax.w_yaxis.line.set_color((0.0, 0.0, 0.0, 0.0))
        self.ax.w_zaxis.line.set_color((0.0, 0.0, 0.0, 0.0))

        self.ax.xaxis.pane.set_edgecolor('white')
        self.ax.yaxis.pane.set_edgecolor('white')
        self.ax.zaxis.pane.set_edgecolor('white')

        self.ax.elev = 1

    def plot_data(self):
        viridis = cm.get_cmap('hsv', 12)
        print(self.wobble_data)

        xs = [value.get('x') for value in self.wobble_data]
        ys = [value.get('y') for value in self.wobble_data]
        zs = [value.get('z') for value in self.wobble_data]
        cs = [value.get('scaled') for value in self.wobble_data]
        self.ax.scatter(xs, ys, zs, c=cs, cmap=viridis, marker='o', alpha=0.4)

    def animate(self, i):
        self.ax.azim += 1




print(WobbleGraph())
