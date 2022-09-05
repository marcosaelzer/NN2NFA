from nn2nfa.translation.automata import Automaton, SumAutomaton
from nn2nfa.translation.automata_utils import join_automata, join_pos_input_multiplier_with_sum, join_multiplier_sum
import math

def build_bruse_multiplier(c: int) -> Automaton:
    c = int(abs(c))
    mult_automaton = Automaton()
    mult_automaton.start_states = {0}
    mult_automaton.end_states = {0}
    mult_automaton.tape_size = 2
    mult_automaton.input_tapes = {0}
    mult_automaton.output_tapes = {1}

    if c == 0:
        mult_automaton.add_edge(0, 0, (1,0))
        mult_automaton.add_edge(0, 0, (0,0))
        return mult_automaton

    for k in range(c):
        x = 1 if (k+c) % 2 == 1 else 0
        next = math.floor((k+c)/2)
        mult_automaton.add_edge(k, next, (1, x))

        x = 1 if k % 2 == 1 else 0
        next = math.floor(k/2)
        mult_automaton.add_edge(k, next, (0,x))

    return mult_automaton

def build_signed_multiplier(c: int) -> Automaton:
    mult_automaton = build_bruse_multiplier(c)
    new_state = mult_automaton.get_number_of_states()
    mult_0_state = new_state + 1
    mult_automaton.start_states = {new_state}

    if c != 0:
        mult_automaton.end_states.add(mult_0_state)
        if c < 0:
            mult_automaton.add_edge(new_state, 0, (0,1))
            mult_automaton.add_edge(new_state, 0, (1,0))
            mult_automaton.add_edge(new_state, mult_0_state, (0,0))

        elif c > 0:
            mult_automaton.add_edge(new_state, 0, (0,0))
            mult_automaton.add_edge(new_state, 0, (1,1))

        mult_automaton.add_edge(mult_0_state, mult_0_state, (0,0))

    else:
        mult_automaton.add_edge(new_state, 0, (0,0))
        mult_automaton.add_edge(new_state, 0, (1,0))

    return mult_automaton


def build_pos_input_multiplier(c: int) -> Automaton:
    mult_automaton = build_bruse_multiplier(c)
    new_state = mult_automaton.get_number_of_states()
    mult_0_state = new_state + 1
    mult_automaton.start_states = {new_state}

    if c != 0:
        mult_automaton.end_states.add(mult_0_state)
        if c < 0:
            mult_automaton.add_edge(new_state, 0, (0,1))
            mult_automaton.add_edge(new_state, mult_0_state, (0,0))

        elif c > 0:
            mult_automaton.add_edge(new_state, 0, (0,0))

        mult_automaton.add_edge(mult_0_state, mult_0_state, (0,0))
    else:
        mult_automaton.add_edge(new_state, 0, (0,0))

    return mult_automaton


def build_pos_input_n_multiplier(weights: list) -> Automaton:
    n = len(weights)
    automaton = Automaton()
    automaton.tape_size = n
    automaton.input_tapes = {i for i in range(n)}
    automaton.output_tapes = set()
    automaton.start_states = {0}
    automaton.end_states = {0}

    for i in range((2 ** (n))):
        b = bin(i).split('b')[1].zfill(n)
        automaton.add_edge(0, 0, tuple(list([int(j) for j in b])))

    automaton = join_automata([0], automaton, build_pos_input_multiplier(weights[0]))
    current_weight_index = 1
    while current_weight_index < n:
        automaton = join_automata([current_weight_index], automaton, build_pos_input_multiplier(weights[current_weight_index]))
        #automaton.minimize()
        current_weight_index += 1
    automaton.minimize()
    for i in range(n):
        automaton.output_tapes.add(n+i)
    return automaton

def build_signed_n_multiplier(weights: list) -> Automaton:
    n = len(weights)
    automaton = Automaton()
    automaton.tape_size = n
    automaton.input_tapes = {i for i in range(n)}
    automaton.output_tapes = set()
    automaton.start_states = {0}
    automaton.end_states = {0}

    for i in range((2 ** n)):
        b = bin(i).split('b')[1].zfill(n)
        automaton.add_edge(0, 0, tuple([int(j) for j in b]))

    automaton = join_automata([0], automaton, build_signed_multiplier(weights[0]))

    current_weight_index = 1
    while current_weight_index < n:
        automaton = join_automata([current_weight_index], automaton, build_signed_multiplier(weights[current_weight_index]))
        #automaton.minimize()
        current_weight_index += 1

    automaton.minimize()
    for i in range(n):
        automaton.output_tapes.add(n+i)
    return automaton


def build_n_adder(n: int, signs: list, res_sign=0, bias=0):
    return SumAutomaton(n, signs, res_sign, bias)


def build_pos_input_lin_comb_automaton(weights: list, bias, activation: str = 'relu'):
    n = len(weights)
    signs = [0 if w >= 0 else 1 for w in weights]
    pos_adder = SumAutomaton(n, signs, 0, bias)
    neg_adder = SumAutomaton(n, signs, 1, bias)
    multiplier = build_pos_input_n_multiplier(weights)

    res_automaton = join_pos_input_multiplier_with_sum(list({i for i in range(multiplier.tape_size)}.difference(multiplier.input_tapes)), multiplier, pos_adder, neg_adder, activation)
    #res_automaton.project_onto_necessary_tapes()
    #res_automaton.minimize()
    return res_automaton

def build_linear_eq_acc(weights: list, bias, leq: bool):
    n = len(weights)
    lin_comb_automaton = build_signed_lin_comb_automaton(weights, bias, activation="id")
    ineq_automaton = Automaton()
    ineq_automaton.start_states = {0}
    ineq_automaton.tape_size = 1
    ineq_automaton.input_tapes = {0}
    if not leq:
        ineq_automaton.end_states = {1}
        ineq_automaton.add_edge(0, 1, (0,))
        ineq_automaton.add_edge(1, 1, (0,))
        ineq_automaton.add_edge(1, 1, (1,))
    else:
        ineq_automaton.end_states = {1, 2}
        ineq_automaton.add_edge(0, 1, (0,))
        ineq_automaton.add_edge(1, 1, (0,))
        ineq_automaton.add_edge(0, 2, (1,))
        ineq_automaton.add_edge(2, 2, (0,))
        ineq_automaton.add_edge(2, 2, (1,))

    automaton = join_automata([n], lin_comb_automaton, ineq_automaton, project_tapes= True)
    #automaton.project_onto_necessary_tapes()
    return automaton

def build_signed_lin_comb_automaton(weights: list, bias, activation: str = 'relu'):
    n = len(weights)
    pos_adder = SumAutomaton(n, None, 0, bias)
    neg_adder = SumAutomaton(n, None, 1, bias)
    multiplier = build_signed_n_multiplier(weights)

    res_automaton = join_multiplier_sum(list({i for i in range(multiplier.tape_size)}.difference(multiplier.input_tapes)),
                                      multiplier, pos_adder, neg_adder, activation)

    res_automaton.minimize()
    return res_automaton

