import time
import glob
from nn2nfa.translation.translate_nn import build_nn_automaton
from nn2nfa.nn_model.toy_nnet import generate_from_file


def do_benchmark(files):
    n = [i for i in range(1, len(files)+1)]
    states = []
    transitions = []
    build_time = []
    for file in files:
        nn = generate_from_file(file)
        print(f'Translating {file}')
        start = time.time()
        automaton = build_nn_automaton(nn, minimize=False)
        end = time.time()
        res_time = end-start
        print(f'Built in {res_time} s')
        print(automaton.get_meta())
        states.append(automaton.get_number_of_states())
        transitions.append(automaton.get_number_of_edges())
        build_time.append(res_time)
        print('#############')

    print(n)
    print(f'States {states}')
    print(f'Transitions {transitions}')
    print(f'Build time {build_time}')




if __name__ == '__main__':
    files = sorted(glob.glob('../assets/benchmark_a/*.toynnet'))
    print(files)
    do_benchmark(files)