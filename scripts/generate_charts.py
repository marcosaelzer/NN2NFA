import matplotlib.pyplot as plt

# specify data line chart
number_of_layers = [1, 2, 3, 4, 5]                        # number of layers of BNN
states = [11, 67, 97, 75847, 474676]            # amount of nodes of resulting nfa
transitions = [19, 126, 208, 109991, 1014886]          # amount of transitions of resulting nfa
build_time = [0.0006601810455322266, 0.001981019973754883, 0.0029799938201904297, 1.5141980648040771, 15.329833030700684] # time to built resulting nfa

# specify data bar chart
automata_number = [1, 2, 3, 4, 5]
states_without_minimization = [79448, 111605, 8359, 6621, 5918]
states_with_minimization = [231, 1454, 856, 136, 813]
percentage_of_reduction = [ int(100 - (after/before) * 100) for before,after in
                            zip(states_without_minimization,states_with_minimization)]
# generate plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,6))
ax3 = ax1.twinx()

ax1.set_yscale('log')
ax1.set_xlabel("number of layers")
ax1.set_ylabel("log. buildtime in s")
ax1.set_title("log.buildtime and automata size per BNN_fix depth")
ax1.set_xticks(number_of_layers)
ax1.plot(number_of_layers, build_time, marker="o", color="tab:orange", label="build time")

ax3.set_yscale('log')
ax3.set_ylabel("log. number states/transitions")
ax3.plot(number_of_layers, states, marker="s", color="tab:green", label="states")
ax3.plot(number_of_layers, transitions, marker="s", color="tab:blue", label="transitions")



ax2.plot(automata_number, percentage_of_reduction, marker="s", color="tab:purple", linestyle="dashed")
ax2.set_xlabel("automata")
ax2.set_ylabel("state set size reduction in %")
ax2.set_title("state set size reduction per automaton")
ax2.set_xticks(automata_number)
ax2.set_yticks([i*10 for i in range(11)])
ax1.legend()
ax3.legend(loc=1)
fig.tight_layout()

# save plot as .png at current location
fig.savefig("experiment.png")