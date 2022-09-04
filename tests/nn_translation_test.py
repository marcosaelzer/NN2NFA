from nn2nfa.translation.translate_nn import build_nn_automaton
from nn2nfa.nn_model.toy_nnet import generate_from_file, ToyNNetwork
from benchmarks.bin_nn_fixed_height import test_on_random_inputs

if __name__ == '__main__':
    toynnet: ToyNNetwork = generate_from_file("../assets/nn_2n_minimal_example1.toynnet")
    print(toynnet)

    a = build_nn_automaton(toynnet)
    print(a)

    print(test_on_random_inputs(toynnet, a))
    print("Output: " + str(toynnet.compute_output([-4])))
    #print(a.is_empty())
    #print(a.test(vec))