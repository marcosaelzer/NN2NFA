from matplotlib import pyplot as plt
def main():
    n = [1, 2, 3, 4, 5, 6, 7]
    nodes = [6, 22, 40, 16, 24, 182, 468]
    edges = [14, 54, 90, 42, 72, 488, 4225]
    build_time = [0.002, 0.03, 0.7, 213, 334, 1915, 6514]

    fig, ax = plt.subplots()
    """axs[0].plot(n, nodes)
    axs[0].set_title('Nodes')
    axs[0].set(xlabel='', ylabel='')
    axs[1].plot(n, edges, 'tab:orange')
    axs[1].set_title('Edges')
    axs[1].set(xlabel='hidden layers', ylabel='')
    axs[2].plot(n, build_time, 'tab:green')
    axs[2].set_title('Built time [sec]')
    axs[2].set(xlabel='', ylabel='')"""

    plt.title('Fixed amount of hidden layers')
    ax.set(xlabel='neurons per hidden layer', ylabel='')
    ax.set(ylabel='nodes and sec')
    ax.plot(n, nodes)
    ax.plot(n, build_time, 'tab:green')

    ax2 = ax.twinx()
    ax2.set(ylabel='edges')
    ax2.plot(n, edges, 'tab:orange')
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    """
    for ax in axs.flat:
        ax.label_outer()
    """
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
