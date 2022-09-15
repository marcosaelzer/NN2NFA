import matplotlib.pyplot as plt

# specify data (hard-coded)
n = [1, 2, 3, 4]                        # number of layers of BNN
nodes = [20, 55, 37, 146]               # amount of nodes of resulting nfa
edges = [50, 142, 111, 3502]            # amount of edges of resulting nfa
build_time = [0.024, 0.91, 1.12, 4.09]  # time to built resulting nfa

# generate plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,6))
ax3 = ax1.twinx()

ax1.set_yscale('log')
ax1.set_xlabel("number of layers")
ax1.set_ylabel("log. buildtime in s")
ax1.set_title("DNN depth vs log.buildtime and automata size")
ax1.set_xticks(n)
ax1.plot(n,build_time, marker="o", color="tab:orange", label="build time")

ax3.set_yscale('log')
ax3.set_ylabel("log. number nodes/edges")
ax3.plot(n,nodes, marker="s", color="tab:green", label="nodes")
ax3.plot(n,edges, marker="s", color="tab:blue", label="edges")

ax2.bar(n,build_time)
ax2.set_xlabel("layer")
ax2.set_ylabel("state size reduction in %")
ax2.set_title("DNN layer automaton vs state size reduction")
ax2.set_xticks(n)
ax1.legend()
ax3.legend(loc=1)
fig.tight_layout()

# save plot as .png at current location
fig.savefig("experiment.png")