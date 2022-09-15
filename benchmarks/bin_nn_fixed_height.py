import time
import glob
from nn2nfa.translation.translate_nn import build_nn_automaton
from nn2nfa.nn_model.toy_nnet import generate_from_file

"""
Test script for translating neural networks where there is a fixed number of hidden layers 
and the neurons per layer are increasing
"""

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
        nodes.append(automaton.get_number_of_states())
        edges.append(automaton.get_number_of_edges())
        build_time.append(res_time)
        print('#############')

    print(n)
    print(f'Nodes {nodes}')
    print(f'Edges {edges}')
    print(f'Build time {build_time}')




if __name__ == '__main__':
    #files = generate_nn(1, 1, 2, 8)
    files = sorted(glob.glob('./fixed_neuro_inc_layer/*.toynnet'))
    print(files)
    do_benchmarks(files)