import glob
from nn2nfa.translation.translate_nn import build_nn_automaton
from nn2nfa.nn_model.toy_nnet import generate_from_file


def do_benchmark(files, minimize: bool):
    n = [i for i in range(1, len(files)+1)]
    nodes = []
    for file in files:
        nn = generate_from_file(file)
        print(f'Translating {file}')
        automaton = build_nn_automaton(nn, minimize)
        print(automaton.get_meta())
        nodes.append(automaton.get_number_of_states())
        print('#############')
    return nodes



if __name__ == '__main__':
    files = sorted(glob.glob('../assets/benchmark_b/*.toynnet'))
    print(files)
    print(f'Translate BNN without Minimization')
    statesA = do_benchmark(files, minimize=False)
    print('#############')
    print('#############')
    print(f'Translate BNN with Minimization')
    statesB = do_benchmark(files, minimize=True)

    print("States without Minimization:", statesA)
    print("States with Minimization:", statesB)
    print("Percentage of Reduction:", [int(100 - (after/before) * 100) for before,after in
                                       zip(statesA, statesB)])