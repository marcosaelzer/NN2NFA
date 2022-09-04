from nn2nfa.translation.automata import Automaton, SumAutomaton

def join_automata(onInputTapes:list, automaton1: Automaton, automaton2: Automaton, project_tapes: bool = False):
    """

    Args:
        *onInputTapes: Tape indexes which contain the input for automaton 2
        automaton1: The source automaton
        automaton2: The automaton to join with

    Returns:
        Joined finite_automata
    """
    if len(onInputTapes) != len(automaton2.input_tapes):
        print(onInputTapes)
        print(automaton2.input_tapes)
        print(automaton2.tape_size)
        raise TypeError("InputDim of finite_automata to join with does not match specified inputTapes")

    joined_automaton = Automaton()

    #product_states = [(a, b) for a in automaton1.start_states for b in automaton2.start_states]
    product_states = dict()
    state_counter = 0
    for a in automaton1.start_states:
        for b in automaton2.start_states:
            product_states[(a,b)] = state_counter
            state_counter += 1
    worklist = set([(a, b) for a in automaton1.start_states for b in automaton2.start_states])
    already_worked = set()
    while len(worklist) != 0:
        s, t = worklist.pop()
        i = product_states[(s, t)]
        already_worked.add((s, t))
        """
        i is the index of the state (s,t) in the joined finite_automata
        """
        if s in automaton1.start_states and t in automaton2.start_states:
            joined_automaton.start_states.add(product_states[(s, t)])
        if s in automaton1.end_states and t in automaton2.end_states:
            joined_automaton.end_states.add(product_states[(s, t)])

        for _, u, x in automaton1.get_edges_from(s):
            matches = automaton2.get_input_tape_matching_successors(t, x, onInputTapes)
            for v, y in matches:
                # remove input tapes from y
                new_y = y
                for tape in sorted(automaton2.input_tapes, reverse=True):
                    y_list = list(new_y)
                    del y_list[tape]
                    new_y = "".join(y_list)

                if (u, v) not in already_worked:
                    worklist.add((u, v))
                if (u, v) not in product_states.keys():
                    product_states[(u, v)] = state_counter
                    state_counter += 1
                if not project_tapes:
                    joined_automaton.add_edge(product_states[(s, t)], product_states[(u,v)], x+new_y)
                else:
                    joined_automaton.add_edge(product_states[(s, t)], product_states[(u, v)], remove_joined_tapes_from_word(x, onInputTapes) + new_y)
    joined_automaton.input_tapes = automaton1.input_tapes
    if not project_tapes:
        joined_automaton.tape_size = automaton1.tape_size + automaton2.tape_size - len(onInputTapes)
        joined_automaton.output_tapes = {i for i in range(automaton1.tape_size, joined_automaton.tape_size)}
    else:
        joined_automaton.tape_size = automaton1.tape_size + automaton2.tape_size - 2*len(onInputTapes)
        print(automaton1.tape_size)
        print(onInputTapes)
        print(automaton2.tape_size)
        joined_automaton.output_tapes = {i for i in range(automaton1.tape_size-len(onInputTapes), joined_automaton.tape_size)}
    return joined_automaton


def join_pos_input_multiplier_with_sum(onInputTapes: list, automaton1: Automaton, pos_sum: SumAutomaton, neg_sum: SumAutomaton, activation="relu"):
    if len(onInputTapes) != pos_sum.tape_size - 1:
        raise TypeError("InputDim of finite_automata to join with does not match specified inputTapes")

    joined_automaton = Automaton()

    # Add signs check state to sum automaton
    idle_state = 'idle'
    signs_check_state_pos = 'sign_check_pos'
    signs_check_state_neg = 'sign_check_neg'

    product_states = dict()
    state_counter = 0
    for a in automaton1.start_states:
        product_states[(a, signs_check_state_pos, signs_check_state_neg)] = state_counter
        state_counter += 1
    worklist = set([(a, signs_check_state_pos, signs_check_state_neg) for a in automaton1.start_states])
    already_worked = set()
    while len(worklist) != 0:
        s, t, t_ = worklist.pop()
        i = product_states[(s, t, t_)]
        already_worked.add((s, t, t_))
        """
        i is the index of the state (s,t) in the joined finite_automata
        """
        if s in automaton1.start_states and t == signs_check_state_pos and t_ == signs_check_state_neg:
            joined_automaton.start_states.add(i)
        if s in automaton1.end_states and (t in pos_sum.end_states or t_ in neg_sum.end_states):
            joined_automaton.end_states.add(i)

        for _, u, x in automaton1.get_edges_from(s):

            if t == signs_check_state_pos and t_ == signs_check_state_neg:
                check = True
                for j, id in enumerate(onInputTapes):
                    if int(x[id]) != pos_sum.signs[j] or int(x[id]) != neg_sum.signs[j]:
                        check = False
                if check:
                    # Case result of sum is positive
                    for next in pos_sum.start_states:
                        if (u, next, idle_state) not in already_worked:
                            worklist.add((u, next, idle_state))
                        if (u, next, idle_state) not in product_states.keys():
                            product_states[(u, next, idle_state)] = state_counter
                            state_counter += 1
                        joined_automaton.add_edge(i, product_states[(u, next, idle_state)], remove_joined_tapes_from_word(x, onInputTapes) + str('0'))

                    # Case result of sum is negative
                    for next in neg_sum.start_states:
                        if (u, idle_state, next) not in already_worked:
                            worklist.add((u, idle_state, next))
                        if (u, idle_state, next) not in product_states.keys():
                            product_states[(u, idle_state, next)] = state_counter
                            state_counter += 1
                        if activation == "relu":
                            joined_automaton.add_edge(i, product_states[(u, idle_state, next)], remove_joined_tapes_from_word(x, onInputTapes) + str('0'))
                        else:
                            joined_automaton.add_edge(i, product_states[(u, idle_state, next)], remove_joined_tapes_from_word(x, onInputTapes) + str('1'))
                    continue
                else:
                    continue
            else:
                if t_ == idle_state:
                    suc, res_bit = pos_sum.get_input_tape_matching_successors(t, x, onInputTapes)
                    if suc is None:
                        continue
                    next = (u, suc, idle_state)
                if t == idle_state:
                    suc, res_bit = neg_sum.get_input_tape_matching_successors(t_, x, onInputTapes)
                    if activation == "relu":
                        res_bit = 0
                    if suc is None:
                        continue
                    next = (u, idle_state, suc)

            if next not in already_worked:
                worklist.add(next)
            if next not in product_states.keys():
                product_states[next] = state_counter
                state_counter += 1
            joined_automaton.add_edge(i, product_states[next], remove_joined_tapes_from_word(x, onInputTapes) + str(res_bit))

    joined_automaton.input_tapes = automaton1.input_tapes
    joined_automaton.tape_size = automaton1.tape_size - len(onInputTapes) + 1
    joined_automaton.output_tapes = {automaton1.tape_size-len(onInputTapes)}

    return joined_automaton

def join_multiplier_sum(onInputTapes: list, automaton1: Automaton, pos_sum: SumAutomaton, neg_sum: SumAutomaton, acitvation="relu"):
    if len(onInputTapes) != pos_sum.tape_size - 1:
        raise TypeError("InputDim of finite_automata to join with does not match specified inputTapes")

    joined_automaton = Automaton()

    # Add signs check state to sum automaton
    idle_state = 'idle'
    signs_check_state_pos = 'sign_check_pos'
    signs_check_state_neg = 'sign_check_neg'

    product_states = dict()
    state_counter = 0
    for a in automaton1.start_states:
        product_states[(a, signs_check_state_pos, signs_check_state_neg, ())] = state_counter
        state_counter += 1
    worklist = set([(a, signs_check_state_pos, signs_check_state_neg, ()) for a in automaton1.start_states])
    already_worked = set()
    while len(worklist) != 0:
        s, t, t_, sign_situation = worklist.pop()
        i = product_states[(s, t, t_, sign_situation)]
        already_worked.add((s, t, t_, sign_situation))
        """
        i is the index of the state (s,t) in the joined finite_automata
        """
        if s in automaton1.start_states and t == signs_check_state_pos and t_ == signs_check_state_neg:
            joined_automaton.start_states.add(i)
        if s in automaton1.end_states and (t in pos_sum.end_states or t_ in neg_sum.end_states):
            joined_automaton.end_states.add(i)

        for _, u, x in automaton1.get_edges_from(s):

            if t == signs_check_state_pos and t_ == signs_check_state_neg:
                signs = []
                only_pos_check = True
                only_neg_check = True
                for index in onInputTapes:
                    if x[index] == "0":
                        signs.append(0)
                        only_neg_check = False
                    else:
                        signs.append(1)
                        only_pos_check = False
                signs = tuple(signs)

                # Case result of sum is positive
                if not only_neg_check:
                    for next in pos_sum.start_states:
                        new_state = (u, next, idle_state, signs)
                        if  new_state not in already_worked:
                            worklist.add(new_state)
                        if new_state not in product_states.keys():
                            product_states[new_state] = state_counter
                            state_counter += 1
                        joined_automaton.add_edge(i, product_states[new_state], remove_joined_tapes_from_word(x, onInputTapes) + str('0'))

                # Case result of sum is negative
                if not only_pos_check:
                    for next in neg_sum.start_states:
                        new_state = (u, idle_state, next, signs)
                        if new_state not in already_worked:
                            worklist.add(new_state)
                        if new_state not in product_states.keys():
                            product_states[new_state] = state_counter
                            state_counter += 1
                        if acitvation == "relu":
                            joined_automaton.add_edge(i, product_states[new_state], remove_joined_tapes_from_word(x, onInputTapes) + str('0'))
                        else:
                            joined_automaton.add_edge(i, product_states[new_state], remove_joined_tapes_from_word(x, onInputTapes) + str('1'))
                continue
            else:
                if t_ == idle_state:
                    suc, res_bit = pos_sum.get_input_tape_matching_successors(t, x, onInputTapes, sign_situation=sign_situation)
                    if suc is None:
                        continue
                    next = (u, suc, idle_state, sign_situation)
                if t == idle_state:
                    suc, res_bit = neg_sum.get_input_tape_matching_successors(t_, x, onInputTapes, sign_situation=sign_situation)
                    if acitvation == "relu":
                        res_bit = 0
                    if suc is None:
                        continue
                    next = (u, idle_state, suc, sign_situation)

            if next not in already_worked:
                worklist.add(next)
            if next not in product_states.keys():
                product_states[next] = state_counter
                state_counter += 1
            joined_automaton.add_edge(i, product_states[next], remove_joined_tapes_from_word(x, onInputTapes) + str(res_bit))

    joined_automaton.input_tapes = automaton1.input_tapes
    joined_automaton.tape_size = automaton1.tape_size - len(onInputTapes) + 1
    joined_automaton.output_tapes = {automaton1.tape_size-len(onInputTapes)}

    return joined_automaton

def remove_joined_tapes_from_word(x: str, joined_tapes: list):
    new = []
    for i in range(len(x)):
        if i not in joined_tapes:
            new.append(x[i])
    return "".join(new)