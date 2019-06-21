import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import matplotlib


def Make_animation(npy_file):
    all_particle_data = np.load(npy_file)
    n_iterations = all_particle_data.shape[0]
    n_particles = all_particle_data.shape[1]
    all_particle_data = all_particle_data.T
    nfr = n_iterations  # Number of frames
    fps = 1 # Frame per sec
    xs = []
    ys = []
    zs = []
    ws = []
    for particle in range(n_iterations):
        xs.append(all_particle_data[0].T[particle])
        ys.append(all_particle_data[1].T[particle])
        zs.append(all_particle_data[2].T[particle])
        ws.append(all_particle_data[3].T[particle])

    fig = plt.figure(figsize=(12, 8))

    ax1 = fig.add_subplot(221, projection='3d')
    sct1, = ax1.plot([], [], [], "o", markersize=2)
    ax1.set_xlim(0, 7000)
    ax1.set_ylim(0, 30)
    ax1.set_zlim(0, 50)
    ax1.set_xlabel('PV capacity[W]')
    ax1.set_ylabel('Wind capacity[kW]')
    ax1.set_zlabel('Battery capacity[kW]')
    ax1.set_title('Particle movement XYZ')

    ax2 = fig.add_subplot(222, projection='3d')
    sct2, = ax2.plot([], [], [], "o", markersize=2)
    ax2.set_xlim(0, 7000)
    ax2.set_ylim(0, 30)
    ax2.set_zlim(0, 30)
    ax2.set_xlabel('PV capacity[W]')
    ax2.set_ylabel('Wind capacity[kW]')
    ax2.set_zlabel('Diesel capacity[kW]')
    ax2.set_title('Particle movement XYW')

    ax3 = fig.add_subplot(223, projection='3d')
    sct3, = ax3.plot([], [], [], "o", markersize=2)
    ax3.set_xlim(0, 7000)
    ax3.set_ylim(0, 50)
    ax3.set_zlim(0, 30)
    ax3.set_xlabel('PV capacity[W]')
    ax3.set_ylabel('Battery capacity[kW]')
    ax3.set_zlabel('Diesel capacity[kW]')
    ax3.set_title('Particle movement XZW')

    ax4 = fig.add_subplot(224, projection='3d')
    sct4, = ax4.plot([], [], [], "o", markersize=2)
    ax4.set_xlim(0, 30)
    ax4.set_ylim(0, 50)
    ax4.set_zlim(0, 30)
    ax4.set_xlabel('Wind capacity[W]')
    ax4.set_ylabel('Battery capacity[kW]')
    ax4.set_zlabel('Diesel capacity[kW]')
    ax4.set_title('Particle movement YZW')

    def update(ifrm, xa, ya, za, wa):
        sct1.set_data(xa[ifrm], ya[ifrm])
        sct1.set_3d_properties(za[ifrm])
        sct2.set_data(xa[ifrm], ya[ifrm])
        sct2.set_3d_properties(wa[ifrm])
        sct3.set_data(xa[ifrm], za[ifrm])
        sct3.set_3d_properties(wa[ifrm])
        sct4.set_data(ya[ifrm], za[ifrm])
        sct4.set_3d_properties(wa[ifrm])

    plt.tight_layout()
    ani = animation.FuncAnimation(fig, update, nfr, fargs=(xs,ys,zs,ws), interval=1000/fps)
    fn = 'Result/plot_3d_scatter_funcanimation'
    ani.save(fn + '.gif', fps=fps)
    s = ani.to_jshtml()
    with open('Result/plot_3d_scatter_funcanimation.html', 'w') as f:
        f.write(s)
