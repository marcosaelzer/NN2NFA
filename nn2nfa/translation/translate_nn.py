from typing import List

from nn2nfa.translation.automata_builder import Automaton
from nn2nfa.nn_model.toy_nnet import ToyNNetwork
import nn2nfa.translation.automata_builder as builder
import multiprocessing as mp


def build_neuron_automata_parallel(nn: ToyNNetwork, prev_layer_automaton, layer_index) -> list:

    """ #pool = mp.Pool(mp.cpu_count())
    pool = mp.Pool(1)

    automata = [pool.apply(build_neuron_automaton, args=(prev_layer_automaton,
                                                         nn.get_neuron_weights(layer_index, i),
                                                         nn.get_neuron_bias(layer_index, i),
                                                         nn.get_neuron_activation(layer_index, i),
                                                         i, layer_index))
                for i in range(nn.get_neuron_count(layer_index))]
    pool.close()
    return [element[0] for element in sorted(automata, key=lambda tup: tup[1])]
"""
    return [build_neuron_automaton(prev_layer_automaton,
                                                         nn.get_neuron_weights(layer_index, i),
                                                         nn.get_neuron_bias(layer_index, i),
                                                         nn.get_neuron_activation(layer_index, i),
                                                         i, layer_index) for i in range(nn.get_neuron_count(layer_index))]


def build_neuron_automaton(prev_layer_automaton: Automaton, weights, bias, activation, i, layer_index):
    #print(f"Build neuron Automata for: weights: {weights} and bias: {bias}")
    weights = [int(w) for w in weights]
    bias = int(bias)
    if activation == 'identity':
        raise TypeError('NNs with Identity Activations are currently not supported')

    if layer_index != 0:
        lin_comb_automaton = builder.build_pos_input_lin_comb_automaton(weights, bias, activation)
    else:
        lin_comb_automaton = builder.build_signed_lin_comb_automaton(weights, bias, activation)

    neuron_automaton = builder.join_automata(list(prev_layer_automaton.output_tapes), prev_layer_automaton, lin_comb_automaton)
    neuron_automaton.project_onto_necessary_tapes()
    print(f'Automata layer {layer_index} number {i}')
    neuron_automaton.minimize()
    #print(neuron_automaton)
    #print(neuron_automaton.is_deterministic())
    return neuron_automaton


def build_layer_automaton(neuron_automata: list) -> Automaton:
    joined_automaton = neuron_automata.pop(0)
    while len(neuron_automata) != 0:
        next = neuron_automata.pop(0)
        print('Joine neuron zu layer')
        joined_automaton = builder.join_automata(list(joined_automaton.input_tapes), joined_automaton, next)
        joined_automaton.minimize()
    # ToDo: Make all results output tapes !!!
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
    #print('Input Automaton')
    return automaton

def build_output_properties(props: list):
    if len(props) == 0:
        return

    prop = props.pop()
    current_automaton = builder.build_linear_eq_acc(prop.left_side, -prop.right_side, prop.leq)
    for prop in props:
        prop_automaton = builder.build_linear_eq_acc(prop.left_side, -prop.right_side, prop.leq)
        current_automaton = builder.join_automata(list(current_automaton.input_tapes), current_automaton, prop_automaton)
        current_automaton.input_tapes = {i for i in range(current_automaton.tape_size)}
        current_automaton.output_tapes = {i for i in range(current_automaton.tape_size)}
        current_automaton.minimize()
    current_automaton.input_tapes = {i for i in range(current_automaton.tape_size)}
    current_automaton.output_tapes = {i for i in range(current_automaton.tape_size)}
    return current_automaton


def build_nn_automaton(nn: ToyNNetwork):
    current_automaton = build_id_automaton(nn.input_size)
    for i in range(nn.get_layer_count()):
        neuron_automata = build_neuron_automata_parallel(nn, current_automaton, i)
        current_automaton = build_layer_automaton(neuron_automata)
        print(f'Built layer {i}: with: {current_automaton.get_number_of_states()} states')

    return current_automaton