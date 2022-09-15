import matplotlib.pyplot as plt

# specify data line chart
number_of_layers = [3, 4, 5, 6, 7]                        # number of layers of BNN
nodes = [20, 55, 37, 146, 4642]               # amount of nodes of resulting nfa
edges = [50, 142, 111, 3502, 77765]            # amount of edges of resulting nfa
build_time = [0.024, 0.91, 1.12, 4.09, 3995]  # time to built resulting nfa

# specify data bar chart
layer_number = [1,2,3,4,5,6,7]
states_without_minimization = [4,25,90,255,213,22848,23161]
states_with_minimization = [2,8,13,50,46,4982,4642]
percentage_of_reduction = [ int(100 - (after/before) * 100) for before,after in
                            zip(states_without_minimization,states_with_minimization)
                            ]
# generate plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,6))
ax3 = ax1.twinx()

ax1.set_yscale('log')
ax1.set_xlabel("number of layers")
ax1.set_ylabel("log. buildtime in s")
ax1.set_title("DNN depth vs log.buildtime and automata size")
ax1.set_xticks(number_of_layers)
ax1.plot(number_of_layers, build_time, marker="o", color="tab:orange", label="build time")

ax3.set_yscale('log')
ax3.set_ylabel("log. number nodes/edges")
ax3.plot(number_of_layers, nodes, marker="s", color="tab:green", label="nodes")
ax3.plot(number_of_layers, edges, marker="s", color="tab:blue", label="edges")



ax2.plot(layer_number, percentage_of_reduction, marker="s", color="tab:purple", linestyle="dashed")
ax2.set_xlabel("layer")
ax2.set_ylabel("state size reduction in %")
ax2.set_title("DNN layer automaton vs state size reduction")
ax2.set_xticks(layer_number)
ax2.set_yticks([i*10 for i in range(11)])
ax1.legend()
ax3.legend(loc=1)
fig.tight_layout()

# save plot as .png at current location
fig.savefig("experiment.png")