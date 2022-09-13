import matplotlib.pyplot as plt
import random as ran
import time
import math

from nn2nfa.translation.automata import Automaton
from nn2nfa.translation.translate_nn import build_nn_automaton
from nn2nfa.nn_model.toy_nnet import generate_from_file, ToyNNetwork
"""
Test script for generating and translating neural networks where each hidden layer has a fixed number of neurons
"""
def generate_nn(inputs, outputs, fixed_width, hidden_layers):
    files = []
    for n in range(1, hidden_layers+1):
        filename = f'nn_fixed_width_{fixed_width}_{n}.toynnet'
        f = open(filename, 'w')
        files.append(filename)
        f.write(f'input_size = {inputs} \n')

        for i in range(n):
            ran_weights = [ran.choice([-1, 1]) for _ in range(inputs)]
            ran_bias = ran.choice([-1, 1])
            f.write(f'({ran_weights}, {ran_bias}, relu)')
            if i != n - 1:
                f.write('; ')
            else:
                f.write(' \n')

        for i in range(fixed_width):
            for j in range(n):
                ran_weights = [ran.choice([-1, 1]) for _ in range(n)]
                ran_bias = ran.choice([-1, 1])
                f.write(f'({ran_weights}, {ran_bias}, relu)')
                if j != n - 1:
                    f.write('; ')
                else:
                    f.write(' \n')

        for i in range(outputs):
            ran_weights = [ran.choice([-1, 1]) for _ in range(n)]
            ran_bias = ran.choice([-1, 1])
            f.write(f'({ran_weights}, {ran_bias}, relu)')
            if i != outputs - 1:
                f.write('; ')
            else:
                f.write(' \n')

        f.close()

    return files


def test_on_random_inputs(nn: ToyNNetwork, automaton):
    for k in range(100):
        false_ex: bool = ran.choice([0, 1])
        ran_input = [ran.choice(range(-50, 50)) for _ in range(nn.input_size)]
        ran_bin_input = []
        output = nn.compute_output(ran_input)
        if false_ex:
            output = [r + 1 for r in output]
        output_bin = []
        for z in ran_input:
            bin_z = bin(int(abs(z))).split('b')[1][::-1]
            if z < 0:
                bin_z = "1" + bin_z
            else:
                bin_z = "0" + bin_z
            ran_bin_input.append(bin_z)

        for z in output:
            bin_z = bin(int(abs(z))).split('b')[1][::-1]
            if z < 0:
                bin_z = "1" + bin_z
            else:
                bin_z = "0" + bin_z
            output_bin.append(bin_z)

        test_list = ran_bin_input + output_bin

        max_len = max([len(z) for z in test_list])
        test_list = [z_bin.ljust(max_len, '0') for z_bin in test_list]

        test_w = []

        for j in range(max_len):
            w_list = []
            for w in test_list:
                w_list.append(w[j])
            test_w.append(tuple([int(k) for k in w_list]))

        acc = False
        for i in range(50):
            test_w.append(tuple([0 for _ in range(nn.input_size+nn.output_size)]))
            if automaton.test(test_w):
                acc = True
                break

        if (not acc and not false_ex) or (acc and false_ex):
            print(f'Was false example: {false_ex}')
            print(ran_input)
            print(output)
            print(test_w)
            return False
    return True


def do_benchmarks(files):
    n = [i for i in range(1, len(files)+1)]
    nodes = []
    edges = []
    build_time = []
    for file in files:
        nn = generate_from_file(file)
        print(f'Translating {file}')
        start = time.time()
        automaton = build_nn_automaton(nn, None)
        end = time.time()
        res_time = end-start
        print(f'Built in {res_time} s')
        print(automaton.get_meta())
        print(f'test check: {test_on_random_inputs(nn, automaton)}')
        nodes.append(automaton.get_number_of_states())
        edges.append(automaton.get_number_of_edges())
        build_time.append(res_time)
        print('#############')

    print(n)
    print(nodes)
    print(edges)
    print(build_time)
    fig, ax = plt.subplots()
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
    plt.savefig('fixed_width_plot.png')
    plt.show()




if __name__ == '__main__':
    files = generate_nn(2, 2, 1, 4)
    do_benchmarks(files)