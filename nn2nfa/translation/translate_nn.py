from nn2nfa.translation.automata_builder import Automaton
from nn2nfa.nn_model.toy_nnet import ToyNNetwork
import nn2nfa.translation.automata_builder as builder


def build_neuron_automaton(prev_layer_automaton: Automaton, weights, bias, activation, i, layer_index, minimize):
    weights = [int(w) for w in weights]
    bias = int(bias)

    if layer_index != 0:
        lin_comb_automaton = builder.build_pos_input_lin_comb_automaton(weights, bias, minimize, activation)
    else:
        lin_comb_automaton = builder.build_signed_lin_comb_automaton(weights, bias, minimize, activation)

    neuron_automaton = builder.join_automata(list(prev_layer_automaton.output_tapes), prev_layer_automaton,
                                             lin_comb_automaton)
    neuron_automaton.project_onto_necessary_tapes()

    if minimize:
        neuron_automaton.minimize()

    return neuron_automaton


def build_layer_automaton(neuron_automata: list, layer_index, minimize: bool) -> Automaton:
    joined_automaton = neuron_automata.pop(0)
    while len(neuron_automata) != 0:
        next = neuron_automata.pop(0)
        joined_automaton = builder.join_automata(list(joined_automaton.input_tapes), joined_automaton, next)
        if minimize:
            joined_automaton.minimize()
    full_set = {i for i in range(joined_automaton.tape_size)}
    new_outputs = full_set.difference(joined_automaton.input_tapes)
    joined_automaton.output_tapes = new_outputs
    return joined_automaton


def build_id_automaton(input_size):
    automaton = Automaton()
    automaton.tape_size = input_size
    automaton.input_tapes = {i for i in range(input_size)}
    automaton.output_tapes = {i for i in range(input_size)}
    automaton.start_states = {0}
    automaton.end_states = {0}
    for i in range((2 ** input_size)):
        b = bin(i).split('b')[1].zfill(input_size)
        automaton.add_edge(0, 0, tuple(list([int(j) for j in b])))
    return automaton


def build_nn_automaton(nn: ToyNNetwork, minimize: bool):
    current_automaton = build_id_automaton(nn.input_size)
    for layer_index in range(nn.get_layer_count()):
        neuron_automata = [build_neuron_automaton(current_automaton,
                                                  nn.get_neuron_weights(layer_index, i),
                                                  nn.get_neuron_bias(layer_index, i),
                                                  nn.get_neuron_activation(layer_index, i),
                                                  i, layer_index, minimize) for i in range(nn.get_neuron_count(layer_index))]
        current_automaton = build_layer_automaton(neuron_automata, layer_index, minimize)

    return current_automaton
