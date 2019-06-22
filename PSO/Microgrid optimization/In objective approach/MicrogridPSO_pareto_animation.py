import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import matplotlib.colors
from matplotlib.cm import ScalarMappable, get_cmap


def Make_animation(npy_file):
    all_particle_data_with_cost = np.load(
        "Result/all_particle_data_with_cost.npy")
    all_particle_data_with_cost = all_particle_data_with_cost.T
    n_iterations = all_particle_data_with_cost.shape[0]
    n_particles = all_particle_data_with_cost.shape[1]
    range_max = [10000, 100, 100, 100, 100000000]

    nfr = n_iterations  # Number of frames
    fps = 1  # Frame per sec
    xs = []
    ys = []
    zs = []
    ws = []
    vs = []
    for iteration in range(n_iterations):
        xs.append(all_particle_data_with_cost[0].T[iteration])
        ys.append(all_particle_data_with_cost[1].T[iteration])
        zs.append(all_particle_data_with_cost[2].T[iteration])
        ws.append(all_particle_data_with_cost[3].T[iteration])
        vs.append(all_particle_data_with_cost[4].T[iteration])

    def Convert_int(ndarray):
        return ndarray.astype(np.int32)

    norm = matplotlib.colors.Normalize(vmin=np.min(vs), vmax=np.max(vs))
    vs = list(map(Convert_int, vs))

    # %% Create Color Map
    cmap = get_cmap('jet')
    norm = matplotlib.colors.Normalize(vmin=np.min(vs), vmax=np.max(vs))
    mappable = ScalarMappable(cmap=cmap, norm=norm)
    mappable._A = []

    fig = plt.figure(figsize=(24, 13))

    ax1 = fig.add_subplot(232, projection=Axes3D.name)
    ax2 = fig.add_subplot(233, projection=Axes3D.name)
    ax3 = fig.add_subplot(235, projection=Axes3D.name)
    ax4 = fig.add_subplot(236, projection=Axes3D.name)

    def update(ifrm, xa, ya, za, wa, va):
        ax1.cla()
        ax2.cla()
        ax3.cla()
        ax4.cla()
        for particle in range(n_particles):
            # ax1
            ax1.scatter(
                xa[ifrm][particle],
                ya[ifrm][particle],
                za[ifrm][particle],
                s=70,
                color=cmap(
                    norm(
                        va[ifrm][particle])),
                marker='o')
            ax1.set_title('Particle XYZ iterations = ' + str(ifrm + 1) +
                          " Global best =" + str(np.max(va[ifrm])), y=1.0)
            ax1.set_xlim(0, range_max[0])
            ax1.set_ylim(0, range_max[1])
            ax1.set_zlim(0, range_max[2])
            ax1.set_xlabel('PV capacity[W]')
            ax1.set_ylabel('Wind capacity[kW]')
            ax1.set_zlabel('Battery capacity[kW]')
            # ax2
            ax2.scatter(
                xa[ifrm][particle],
                ya[ifrm][particle],
                wa[ifrm][particle],
                s=70,
                color=cmap(
                    norm(
                        va[ifrm][particle])),
                marker='o')
            ax2.set_title('Particle movement XYW iterations = ' +
                          str(ifrm +
                              1) +
                          " Global best =" +
                          str(np.max(va[ifrm])), y=1.0)
            ax2.set_xlim(0, range_max[0])
            ax2.set_ylim(0, range_max[1])
            ax2.set_zlim(0, range_max[3])
            ax2.set_xlabel('PV capacity[W]')
            ax2.set_ylabel('Wind capacity[kW]')
            ax2.set_zlabel('Diesel capacity[kW]')
            # ax3
            ax3.scatter(
                xa[ifrm][particle],
                za[ifrm][particle],
                wa[ifrm][particle],
                s=70,
                color=cmap(
                    norm(
                        va[ifrm][particle])),
                marker='o')
            ax3.set_title('Particle movement XXW iterations = ' +
                          str(ifrm +
                              1) +
                          " Global best =" +
                          str(np.max(va[ifrm])), y=1.0)
            ax3.set_xlim(0, range_max[0])
            ax3.set_ylim(0, range_max[2])
            ax3.set_zlim(0, range_max[3])
            ax3.set_xlabel('PV capacity[W]')
            ax3.set_ylabel('Battery capacity[kW]')
            ax3.set_zlabel('Diesel capacity[kW]')

            # ax4
            ax4.scatter(
                ya[ifrm][particle],
                za[ifrm][particle],
                wa[ifrm][particle],
                s=70,
                color=cmap(
                    norm(
                        va[ifrm][particle])),
                marker='o')
            ax4.set_title('Particle movement YZW iterations = ' +
                          str(ifrm +
                              1) +
                          " Global best =" +
                          str(np.max(va[ifrm])), y=1.0)
            ax4.set_xlim(0, range_max[1])
            ax4.set_ylim(0, range_max[2])
            ax4.set_zlim(0, range_max[3])
            ax4.set_xlabel('Wind capacity[W]')
            ax4.set_ylabel('Battery capacity[kW]')
            ax4.set_zlabel('Diesel capacity[kW]')
            plt.tight_layout()

    colorbar_ax = fig.add_axes([0.24, 0.1, 0.05, 0.7])
    colorbar = fig.colorbar(mappable, cax=colorbar_ax, shrink=0.5)
    ticks = np.linspace(np.min(vs), np.max(vs), 5)
    colorbar.set_ticks(ticks)
    colorbar.ax.set_yticklabels([str(int(s)) + "[yen]" for s in ticks])

    ani = animation.FuncAnimation(
        fig, update, nfr, fargs=(
            xs, ys, zs, ws, vs), interval=1000 / fps)

    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=fps, metadata=dict(artist='Yuichiro'))

    ani.save('Result/plot_3d_scatter_funcanimation.mp4', writer=writer)

    s = ani.to_jshtml()
    with open('Result/plot_3d_scatter_funcanimation.html', 'w') as f:
        f.write(s)
