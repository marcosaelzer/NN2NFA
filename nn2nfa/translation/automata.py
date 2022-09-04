
from collections import defaultdict
from nn2nfa.translation.FatStateSet import FatStateSet, WorkList
from functools import partial
import time
def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(partial(nested_dict, n-1, type))


class SumAutomaton:
    def __init__(self, n, signs = None, res_sign = 0, bias = 0):
        self.n = n
        self.trans = dict()
        self.start_states = set()
        self.end_states = set()
        self.tape_size = n + 1
        self.signs = signs

        if self.signs is not None and (len(self.signs) != self.n or res_sign not in [0, 1]):
            raise ValueError("SumAutomaton Generation failed, due to invalid sign parameter")
        self.res_sign = res_sign
        self.bias = bias
        self.generate_sum_automaton()

    def generate_sum_automaton(self):
        number_neg = 0
        number_pos = 0
        if self.signs is None:
            number_pos = self.n
            number_neg = self.n
        else:
            for sign in self.signs:
                if sign == 0:
                    number_pos += 1
                if sign == 1:
                    number_neg += 1

        state_ids = [self.bias]
        working_states = {self.bias}
        already_worked = set()
        while len(working_states) != 0:
            i = working_states.pop()
            already_worked.add(i)
            for j in range(-number_neg, number_pos + 1):
                x = (i + j) % 2
                if self.res_sign == 0:
                    k = (i + (j - x)) // 2
                else:
                    k = (i + (j + x)) // 2
                if k not in state_ids:
                    state_ids.append(k)
                if state_ids.index(i) not in self.trans.keys():
                    self.trans[state_ids.index(i)] = {(j, x): state_ids.index(k)}
                else:
                    self.trans[state_ids.index(i)][(j, x)] = state_ids.index(k)
                if k not in already_worked:
                    working_states.add(k)

        self.start_states.add(state_ids.index(self.bias))
        if 0 in state_ids:
            #    state_ids.append(0)
            self.end_states.add(state_ids.index(0))

    def test(self, w) -> bool:
        """
        Method to test a Sum Automaton on a given input word.
        Return True if the input is accepted by the NFA, otherwise returns false
        Args:
            w: The input word

        Returns:

        """
        for c in w:
            if len(c) != self.tape_size:
                return False

        for start in self.start_states:
            current_state = start
            for c in w:
                bit_sum = 0
                res_bit = int(c[len(c) - 1])
                for i in range(len(c) -1):
                    bit_sum += int(c[i]) if self.signs[i] == 0 else -int(c[i])
                if (bit_sum, res_bit) in self.trans[current_state].keys():
                    current_state = self.trans[current_state][(bit_sum, res_bit)]
                else:
                    return False

            if current_state in self.end_states:
                return True

        return False

    def get_input_tape_matching_successors(self, state, symbol, matching_tapes, sign_situation=None):
        signs_to_use = self.signs
        if sign_situation is not None:
            signs_to_use = sign_situation
        bit_sum = 0
        for index, i in enumerate(matching_tapes):
            bit_sum += int(symbol[i]) if signs_to_use[index] == 0 else -int(symbol[i])
        for t in self.trans[state].keys():
            if bit_sum == t[0]:
                return self.trans[state][(bit_sum, t[1])], t[1]
        return None, -1

    def get_number_of_states(self):
        return len(self.trans.keys())


class Automaton:
    def __init__(self):
        self.states: set = set()
        self.successors: defaultdict = nested_dict(2, set)
        self.predecessors: defaultdict = nested_dict(2, set)
        self.tape_size: int = 0
        self.end_states: set = set()
        self.start_states: set = set()
        self.alphabet: set = set()
        self.input_tapes = set()
        self.output_tapes = set()

    def test(self, w) -> bool:
        """
        Method to test a NFA on a given input word.
        Return True if the input is accepted by the NFA, otherwise returns false
        Args:
            w: The input word

        Returns:

        """
        for c in w:
            if len(c) != self.tape_size:
                return False

        working_states = self.start_states.copy()
        for c in w:
            working_states_new = set()
            while len(working_states) != 0:
                state = working_states.pop()
                next = self.get_successors(state, c)
                working_states_new.update(next)
            working_states = working_states_new

        for s in self.end_states:
            if s in working_states:
                return True

        return False

    def is_empty(self) -> bool:
        worklist: set = self.start_states.copy()
        marked: set = set()
        while len(worklist) != 0:
            if set.intersection(worklist, self.end_states) != 0:
                return False
            current_state = worklist.pop()
            marked.add(current_state)
            worklist.union(set.difference(self.get_all_successors(current_state), marked))
        return True


    def project_tapes(self, tapes):
        """
        Implementation of the projection operation on multi-tape NFA.
        Method projects the n-tape NFA to a (n-k)-tape NFA by deleting all tapes in the tapes list

        Args:
            *tapes: List of tape indexes, which will be deleted

        Returns:

        """
        old_graph_states = self.states
        old_graph_successors = self.successors
        old_tape_size = self.tape_size
        old_start_states = self.start_states
        old_end_states = self.end_states
        self.reset()
        for s in old_graph_states:
            for w in old_graph_successors[s].keys():
                for t in old_graph_successors[s][w]:
                #for w in old_graph[s][t].keys():
                    new_w = w
                    for tape in sorted(tapes, reverse=True):
                        w_list = list(new_w)
                        del w_list[tape]
                        new_w = "".join(w_list)
                        if tape in self.input_tapes:
                            self.input_tapes.remove(tape)
                        if tape in self.output_tapes:
                            self.output_tapes.remove(tape)
                    self.add_edge(s, t, new_w)

        self.start_states = old_start_states
        self.end_states = old_end_states
        self.tape_size = old_tape_size - len(tapes)

    def project_onto_necessary_tapes(self):
        tape_set = set(range(self.tape_size))
        survivor_set = self.input_tapes.union(self.output_tapes)
        tape_set = tape_set.difference(survivor_set)
        self.project_tapes(tape_set)

    """
    ########################################
        Functions for NFA Minimization
    ########################################
    """

    def __reachables(self):
        reachables = set()

        todo = list(self.start_states)
        while todo:
            p = todo.pop(0)
            if not p in reachables:
                reachables.add(p)
                for a in self.alphabet:
                    for q in self.get_successors(p, a):
                        todo.append(q)

        return reachables

    def __productives(self):
        productives = set()

        todo = list(self.end_states)
        while todo:
            q = todo.pop(0)
            if not q in productives:
                productives.add(q)
                for a in self.alphabet:
                    for p in self.get_predecessors(q, a):
                        todo.append(p)
        return productives

    def __shrink_to(self, survivors):
        # find new names for the survivors and rename them accordingly
        i = 0
        new_names = {}
        for q in survivors:
            new_names[q] = i
            i += 1

        #self.__clear_states()

        # reset initial and final states
        ps = self.start_states
        self.__clear_initials()
        for p in ps:
            if p in survivors:
                self.__make_initial(new_names[p])

        qs = self.end_states
        self.__clear_finals()
        for q in qs:
            if q in survivors:
                self.__make_final(new_names[q])

        # reinsert all transitions between survivors
        transitions = self.get_edges()
        self.__clear_transitions()
        for (p, q, a) in transitions:
            if p in survivors and q in survivors:
                self.add_edge(new_names[p], new_names[q], a)

        return self

    def __simulation_pairs(self):
        # returns the set { (p,q) | p ~< q }
        n = self.get_number_of_states()
        fs = self.end_states
        sim = {(p, q) for p in range(n) for q in range(n) if p != q and (p not in fs or q in fs)}
        old_sim = set()
        # turn sim into largest is-simulated-by relation by successively removing pairs (p,q) such that p is not simulated by q
        while sim != old_sim:
            old_sim = sim.copy()
            for (p, q) in old_sim:
                is_simulated = True
                for a in self.alphabet:
                    p_succs = self.get_successors(p, a)
                    q_succs = self.get_successors(q, a)

                    for s in p_succs:
                        found_match = False
                        for t in q_succs:
                            if s == t or (s, t) in sim:
                                found_match = True
                                break

                        if not found_match:
                            is_simulated = False
                            break
                    if not is_simulated:
                        break

                if not is_simulated:
                    sim.discard((p, q))
        return sim

    def simulation_equivalence_pairs(self):
        # returns the set { (p,q) | p ~~ q and p < q }
        simulated_by = self.__simulation_pairs()
        return {(p, q) for (p, q) in simulated_by if p < q and (q, p) in simulated_by}

    def bisimulation_pairs(self):
        # returns the set { (p,q) | p ~ q and p < q }
        n = self.get_number_of_states()
        fs = self.end_states

        sim = {(p, q) for p in range(n - 1) for q in range(p, n) if
               (p not in fs or q in fs) and (p in fs or q not in fs) and p != q}
        old_sim = set()
        # turn sim into largest bisimulation by successively removing pairs (p,q) such that p is not bisimilar to q
        while sim != old_sim:
            old_sim = sim.copy()
            for (p, q) in old_sim:
                is_bisimilar = True
                for a in self.alphabet:
                    p_succs = self.get_successors(p, a)
                    q_succs = self.get_successors(q, a)

                    for s in p_succs:
                        found_match = False
                        for t in q_succs:
                            if s == t or (s, t) in sim or (t, s) in sim:
                                found_match = True
                                break

                        if not found_match:
                            is_bisimilar = False
                            break
                    if not is_bisimilar:
                        break

                    """
                    for t in q_succs:
                        found_match = False
                        for s in p_succs:
                            if s == t or (s, t) in sim or (t, s) in sim:
                                found_match = True
                                break

                        if not found_match:
                            is_bisimilar = False
                            break
                    if not is_bisimilar:
                        break
                    """
                if not is_bisimilar:
                    sim.discard((p, q))
        return sim

    def __merge_states(self, replacements):
        old_edges = self.get_edges().copy()
        for (p, q, a) in old_edges:
            p1 = replacements[p]
            q1 = replacements[q]
            if p1 != p or q1 != q:
                self.remove_edge(p, q, a)
                self.add_edge(p1, q1, a)
        return self

    def bisimulation_pairs_worklist(self):
        # returns the set { (p,q) | p ~ q and p < q }

        n = self.get_number_of_states()

        # dictionary that contains successively refined k-bisimulations
        bisim = {}

        def __looks_bisimilar(p: int, q: int):
            nonlocal bisim
            if p == q:
                return True
            (p, q) = (min(p, q), max(p, q))
            if p in bisim:
                return bisim[p].contains(q)
            else:
                return False

        def __is_one_step_bisimilar(p: int, q: int):
            found = True
            for a in self.alphabet:
                ps = self.get_successors(p, a)
                qs = self.get_successors(q, a)
                for p1 in ps:
                    found = False
                    for q1 in qs:
                        if __looks_bisimilar(p1, q1):
                            found = True
                            break
                    if not found:
                        break
                if not found:
                    break
                for q1 in qs:
                    found = False
                    for p1 in ps:
                        if __looks_bisimilar(p1, q1):
                            found = True
                            break
                    if not found:
                        break
                if not found:
                    break
            return found

        def __separate(p: int, q: int):
            nonlocal bisim
            if p < q and p in bisim:
                ps = bisim[p]
                ps.remove_state(q)
                bisim[p] = ps
                for r in ps:
                    if r < q:
                        ps = bisim[r]
                        ps.remove_state(q)
                        bisim[r] = ps
                for i in range(0, p):
                    ps = bisim[i]
                    if ps.contains(p) and ps.contains(q):
                        ps.remove_state(q)
                        bisim[i] = ps

        # start with the largest 0-bisimulation where p ~0 q iff (p in F iff q in F)
        # represented as a map p -> { q | q > p and p ~0 q }
        finals = FatStateSet()
        nonfinals = FatStateSet()
        for i in range(n):
            if i in self.get_finals():
                finals.add_state(i)
            else:
                nonfinals.add_state(i)

        # build the initial worklist of all a-predecessors of any (p,q) s.t. p ~/0 q, for any a
        worklist = WorkList()

        def __schedule_predecessor_pairs(p: int, q: int):
            for p1 in self.get_all_predecessors(p):
                for q1 in self.get_all_predecessors(q):
                    worklist.add_pair(p1, q1)

        for p in finals:
            for q in nonfinals:
                __schedule_predecessor_pairs(p, q)

        # complete the 0-bisimulation ~0 in the maps finals / nonfinals
        for i in range(n):
            if i in finals:
                finals.intersect_from(i + 1)
                bisim[i] = finals.copy()
            else:
                nonfinals.intersect_from(i + 1)
                bisim[i] = nonfinals.copy()

        # successively refine ~0 to the largest bisimulation ~
        while not worklist.is_empty():
            (p, q) = worklist.take_next_pair()
            if p != q:
                #print(f"Now working: {p}, {q}")
                lb = __looks_bisimilar(p, q)
                one_step = __is_one_step_bisimilar(p, q)
                #print(f"Looks bisimilar: {lb}, One Step: {one_step}")
                if lb and not one_step:
                    __separate(p, q)
                    __schedule_predecessor_pairs(p, q)

        return bisim

    def minimize(self):
        states_before = self.get_number_of_states()
        time_before = time.time()
        # minimisation via some simulation-based equivalence quotienting
        if self.get_number_of_states() > 10000:
            return
        # merge pairs of equivalent states, using smallest state as representative of equivalence class
        replacements = {p: p for p in range(0, self.get_number_of_states())}

        """
        if NFA.minimization_engine == NFA.SIMUEQ:
            mergable = self.simulation_equivalence_pairs()
        elif NFA.minimization_engine == NFA.BISIMU:
            mergable = self.bisimulation_pairs()
        """
        #mergable = self.simulation_equivalence_pairs()
        mergable = self.bisimulation_pairs()
        #mergable = self.bisimulation_pairs_worklist()
        """
        for p in mergable.keys():
            for q in mergable[p]:
                r = replacements[q]
                if p < r:
                    replacements[q] = p
        self.__merge_states(replacements)
        """
        for (p,q) in mergable:
            r = replacements[q]
            if p < r:
                replacements[q] = p
        self.__merge_states(replacements)

        # if s <=> t and s<t and t is initial, then s becomes initial now
        new_initials = {replacements[t] for t in self.start_states}
        self.__clear_initials()
        for s in new_initials:
            self.__make_initial(s)

        self.__shrink_to(self.__reachables())

        #print(f'minimized from {states_before} to {self.get_number_of_states()} by {1-self.get_number_of_states()/states_before}% in {time.time()-time_before}s')
        return self

    """
    #################################################
        Helper Functions for manipulating automaton
    #################################################
    """

    def get_successors(self, p, a) -> set:
        successors = set()
        """for _, t, w in self.graph.out_edges(p, keys=True):
            if w == a:
                successors.add(t)"""

        return self.successors[p][a]

    def get_input_tape_matching_successors(self, p, a, tapes) -> set:
        """

        Args:
            p:
            a:
            *tapes:

        Returns:

        """
        edge_set = set()
        for _, u, w in self.get_edges_from(p):
            flag = True
            for i, tape in enumerate(self.input_tapes):
                if w[tape] != a[tapes[i]]:
                    flag = False
            if flag:
                edge_set.add((u, w))
        return edge_set

    def get_number_of_states(self):
        return len(self.states)

    def get_predecessors(self, q, a):
        predecessors = set()
        """for s, _, w in self.graph.in_edges(q, keys=True):
            if w == a:
                predecessors.add(s)"""
        return self.predecessors[q][a]

    def add_edge(self, s: int, t: int, w: str):
        """
        Adds an edge to our automaton
        Args:
            s: Source State
            t: Target State
            w: alphabet symbol

        Returns:

        """
        self.states.add(s)
        self.states.add(t)
        self.alphabet.add(w)
        self.successors[s][w].add(t)
        self.predecessors[t][w].add(s)

        #self.graph.add_edge(s, t, w)
        self.alphabet.add(w)

    def reset(self):
        #self.graph = nx.MultiDiGraph()
        self.states = set()
        self.predecessors = nested_dict(2, set)
        self.successors = nested_dict(2, set)
        self.tape_size = 0
        self.start_states = set()
        self.end_states = set()
        self.alphabet = set()

    def get_edges(self):
        return {(p, q, a) for p in self.states for a in self.successors[p].keys() for q in self.successors[p][a]}

    def get_edges_from(self, state: int):
        """
        edge_set = set()
        for s, t, w in self.graph.edges:
            if s == state:
                edge_set.add((t, w))
        """
        sets = [{(state, t, w) for t in self.successors[state][w]} for w in self.successors[state].keys()]
        return set.union(*sets)


    def __clear_initials(self):
        self.start_states = set()

    def __make_initial(self, p):
        self.start_states.add(p)

    def __clear_finals(self):
        self.end_states = set()

    def __make_final(self, p):
        self.end_states.add(p)

    def __clear_transitions(self):
        self.states = set()
        self.predecessors = nested_dict(2, set)
        self.successors = nested_dict(2, set)

    def remove_edge(self, p, q, a):
        self.successors[p][a].remove(q)
        self.predecessors[q][a].remove(p)

    def get_finals(self):
        return self.end_states

    def get_all_predecessors(self, p):
        return {s for w in self.predecessors[p].keys() for s in self.predecessors[p][w]}

    def get_all_successors(self, p):
        return {s for w in self.successors[p].keys() for s in self.successors[p][w]}

    def __str__(self):
        out_str = f'{len(self.states)} states and {len(self.get_edges())} edges \n'
        out_str += f'tape_size: {self.tape_size}, input_tapes: {self.input_tapes}, output_tapes: {self.output_tapes} \n'
        out_str += f'start: {self.start_states}, end: {self.end_states} \n'
        for state in self.states:
            out_str += f'{state}: ' + r"{"
            for w in self.successors[state].keys():
                out_str += f'{w}: ' + str(self.successors[state][w]) + ', '
            out_str += r'}' + '\n'
        return out_str

    def get_meta(self):
        out_str = f'{len(self.states)} states and {len(self.get_edges())} edges'
        return out_str

    def get_number_of_edges(self):
        return len(self.get_edges())

    def is_deterministic(self):
        for s in self.states:
            for w in self.successors[s].keys():
                if len(self.successors[s][w]) != 1:
                    return False
        return True