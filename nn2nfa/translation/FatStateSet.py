# class to represent sets of intervals of non-negative integers
# currently based on simple ordered lists
# TODO: change to balanced search-tree implementation
from collections import defaultdict
import bisect

class FatStateSet:
    # a fat set is a list of non-negative integer pairs [(a_1,b_1),(a_2,b_2),...,(a_n,b_n)]
    # satisfying a_i <= b_i and b_i < a_(i+1)-1 for all i=1,..,n-1
    # and representing the set {a_1,..,b_1,a_2,..,b_2,...,a_n..,b_n}

    states = []
    lefts = []
    rights = dict()

    def __init__(self):
        self.states = []
        self.lefts = []
        self.rights = dict()
#        return self

#    def __init__(self, p:int, q:int):
#        self.states = [(p,q)]
#        return self

#    def __init__(self, st:list):
#        self.states = st
#        return self

    # used to make a FatSet iterable
    current_interval = 0
    last_iterate = -1

    def is_empty(self):
        return self.lefts == []

    def __reset_iterator(self):
        current_interval=0
        last_iterate = -1

    def show(self):
        """
        return a human-readable string representation of this fat set
        :return:
        """
        s = "{"
        first = True
        for a in self.lefts:
            b = self.rights[a]
            if not first:
                s += ","
            first = False
            if a == b:
                s += str(a)
            else:
                s += str(a) + ",..," + str(b)
        s += "}"
        return s

    def find_nearest_begin(self, x):
        return bisect.bisect(self.lefts, x)-1

    def contains(self, q:int):
        """
        checks whether state q is contained in this fat set
        :param q:
        :return:
        """
        index = self.find_nearest_begin(q)
        if index == -1:
            return False
        a = self.lefts[index]
        b = self.rights[a]
        if a <= q <= b:
            return True
        return False

    def lefts_contain(self, q):
        i = bisect.bisect_left(self.lefts, q)
        if i != len(self.lefts) and self.lefts[i] == q:
            return i
        return -1
    def contains_rec(self, q) -> bool:
        def contains_helper(q, l, r):
            m = (l+r) //2
            (a, b) = self.states[m]
            if a <= q <= b:
                return True
            elif l == r:
                return False
            elif q < a:
                if m == l:
                    return False
                return contains_helper(q, l, m-1)
            else:
                if m == len(self.states) - 1:
                    return False
                return contains_helper(q, m+1, r)

        if len(self.states) == 0:
            return False
        else:
            return contains_helper(q, 0, len(self.states)-1)

    def add_state(self, q):
        if len(self.lefts) == 0:
            self.lefts.append(q)
            self.rights[q] = q
        index = self.find_nearest_begin(q)
        if index == -1:
            a = self.lefts[0]
            if q == a-1:
                self.lefts[0] = q
                self.rights[q] = self.rights[a]
                del self.rights[a]
            else:
                self.lefts.insert(0, q)
                self.rights[q] = q

        a = self.lefts[index]
        b = self.rights[a]
        if a <= q and q <= b:
            return
        elif b + 1 == q:
            self.rights[a] = q
            res = self.lefts_contain(q+1)
            if res != -1:
                self.rights[a] = self.rights[q+1]
                self.lefts.pop(res)
                del self.rights[q+1]
        elif q > b+1:
            res = self.lefts_contain(q + 1)
            if res != -1:
                self.lefts.pop(res)
                self.lefts.insert(res, q)
                self.rights[q] = self.rights[q+1]
                del self.rights[q+1]
            else:
                bisect.insort(self.lefts, q)
                self.rights[q] = q

        self.__reset_iterator()

    def add_state_rec(self, q):
        def add_state_helper(q, l, r):
            m = (l + r) // 2
            (a, b) = self.states[m]
            if a <= q <= b:
                return
            elif b < q-1:
                if m == len(self.states) - 1:
                    self.states.append((q,q))
                    return
                elif q < self.states[m+1][0]-1:
                    self.states.insert(m+1, (q, q))
                    return
                add_state_helper(q, m+1, r)
            elif a > q+1:
                if m == 0:
                    self.states.insert(m, (q,q))
                    return
                elif q > self.states[m-1][1]+1:
                    self.states.insert(m, (q,q))
                    return
                add_state_helper(q, l, m-1)
            elif q == a-1:
                if m == 0:
                    self.states[m] = (q,b)
                else:
                    (c,d) = self.states[m-1]
                    if d == q-1:
                        self.states[m-1] = (c,b)
                        self.states.pop(m)
                    else:
                        self.states[m] = (q,b)
                return
            elif q == b+1:
                if m == len(self.states) - 1:
                    self.states[m] = (a,q)
                else:
                    (c,d) = self.states[m+1]
                    if c == q+1:
                        self.states[m+1] = (a,d)
                        self.states.pop(m)
                    else:
                        self.states[m] = (a,q)
                return


        if len(self.states) == 0:
            self.states.append((q, q))
        add_state_helper(q, 0, len(self.states)-1)
        self.__reset_iterator()

    def add_state_old(self,q:int):
        """
        adds a state to this fat set
        :param q:
        :return:
        """
        i=0
        l=len(self.states)
        done = False
        while i<l and not done:
            (a,b) = self.states[i]
            if b < q-1:
                i+=1
            elif a <= q and q <= b:
                done = True
            elif q == a-1:
                if i == 0:
                    self.states[i] = (q,b)
                else:
                    (c,d) = self.states[i-1]
                    if d == q-1:
                        self.states[i-1] = (c,b)
                        self.states.pop(i)
                    else:
                        self.states[i] = (q,b)
                done = True
            elif q == b+1:
                if i == l-1:
                    self.states[i] = (a,q)
                else:
                    (c,d) = self.states[i+1]
                    if c == q+1:
                        self.states[i+1] = (a,d)
                        self.states.pop(i)
                    else:
                        self.states[i] = (a,q)
                done = True
            elif q < a:
                self.states.insert(i,(q,q))
                done = True
        if not done:
            self.states.append((q,q))
        self.__reset_iterator()

    def add_states(self, p, q):
        if len(self.lefts) == 0:
            self.lefts.append(p)
            self.rights[p] = q
        elif not p <= q:
            return
        elif p == q:
            self.add_state(p)

        index_a = self.find_nearest_begin(p)

        if index_a == -1:
            a = self.lefts[0]
            b = self.rights[a]
            index_a = 0
            if q > b:
                self.lefts[0] = p
                self.rights[p] = self.rights[a]
                del self.rights[a]
            elif q < a - 1:
                self.lefts.insert(0, p)
                self.rights[p] = q
            else:
                self.lefts[0] = p
                self.rights[p] = b
                del self.rights[a]

        a = self.lefts[index_a]
        b = self.rights[a]
        if q <= b:
            return
        else:
            index_b = self.find_nearest_begin(q)
            c = self.lefts[index_b]
            d = self.rights[c]

            if a <= p <= b+1:
                if index_b + 1 < len(self.lefts):
                    next_a = self.lefts[index_b+1]
                else:
                    next_a = -1
                slice = self.lefts[index_a+1: index_b+1]
                tmp = self.lefts.copy()
                self.lefts = tmp[:index_a+1] + tmp[index_b+1:]
                if q > d:
                    if next_a != -1 and q == next_a-1:
                        self.rights[a] = self.rights[next_a]
                        slice.append(next_a)
                        self.lefts.remove(next_a)
                    else:
                        self.rights[a] = q
                else:
                    self.rights[a] = d
                for l in slice:
                    del self.rights[l]
            else:
                if index_b + 1 < len(self.lefts):
                    next_a = self.lefts[index_b+1]
                else:
                    next_a = -1
                slice = self.lefts[index_a+1: index_b + 1]
                tmp = self.lefts.copy()
                self.lefts = tmp[:index_a + 1] + [p] + tmp[index_b + 1:]
                if q > d:
                    if next_a != -1 and q == next_a - 1:
                        self.rights[p] = self.rights[next_a]
                        slice.append(next_a)
                        self.lefts.remove(next_a)
                    else:
                        self.rights[p] = q
                else:
                    self.rights[p] = d
                for l in slice:
                    del self.rights[l]

        self.__reset_iterator()


    def add_states_old(self, p:int, q:int):
        """
        adds the range {p,...,q} to this fat set
        :param p:
        :param q:
        :return:
        """
        low = p
        high = q
        i = 0
        done = False
        while i < len(self.states) and not done:
            (a,b) = self.states[i]
            if b < low-1:
                # case [a,b] before [p,q] ==> go to next
                i += 1
            elif a < low and b <= high:
                # case [a,b] left-overlaps or left-meets [low,high]
                # ==> remove former, go on to insert [a,high]
                self.states.pop(i)
                low = a
            elif a <= high+1 and high <= b:
                # case [a,b] right-overlaps or right-meets [low,high]
                # ==> remove former, go on to insert [low,b]
                self.states.pop(i)
                high = b
            elif a <= low and high <= b:
                # case [low,high] contained in [a,b] ==> nothing to add
                done = True
            elif a >= low and b <= high:
                # case [a,b] contained in [low,high] ==> remove [a,b], implicitly go to next
                self.states.pop(i)
            elif a > high+1:
                # case [a,b] behind [low,high] ==> insert [low,high]
                self.states.insert(i,(low,high))
                done = True
        if not done:
            self.states.append((low,high))
        self.__reset_iterator()

    def remove_state(self, q):
        index = self.find_nearest_begin(q)
        if index == -1:
            return
        a = self.lefts[index]
        b = self.rights[a]
        if a == q:
            self.lefts.pop(index)
            if a!=b:
                self.lefts.insert(index, a+1)
                self.rights[a+1] = self.rights[a]
            del self.rights[a]
        elif a < q < b:
            self.rights[a] = q-1
            self.lefts.insert(index+1, q+1)
            self.rights[q+1] = b
        elif b == q:
            self.rights[a] = b-1
        elif q > b:
            return

    def remove_state_old(self,q:int):
        """
        removes state q from this fat set; leaves it unchanged if q is not contained
        :param q:
        :return:
        """
        i=0
        l=len(self.states)
        done = False
        while i<l and not done:
            (a,b) = self.states[i]
            if q < a:
                done = True
            elif q > b:
                i += 1
            elif q == a and q == b:
                self.states.pop(i)
                done = True
            elif q == a:
                self.states[i] = (a+1,b)
                done = True
            elif q == b:
                self.states[i] = (a,b-1)
                done = True
            else:
                self.states[i] = (q+1,b)
                self.states.insert(i,(a,q-1))
                done = True
        self.__reset_iterator()

    def __max(self):
        l = len(self.lefts)
        if l == 0:
            return None
        else:
            return self.rights[l-1]

    def extract_min(self):
        if len(self.lefts) == 0:
            return None
        else:
            a = self.lefts[0]
            b = self.rights[a]
            if a==b:
                self.lefts.pop(0)
                del self.rights[a]
                return a
            else:
                self.lefts[0] = a+1
                self.rights[a+1] = self.rights[a]
                del self.rights[a]
                return a

    def intersect_from(self, q):
        index = self.find_nearest_begin(q)
        a = self.lefts[index]
        b = self.rights[a]
        if q <= b:
            self.lefts[index] = q
            self.rights[q] = self.rights[a]
            del self.rights[a]
        else:
            index += 1
        for i in range(index):
            del self.rights[self.lefts[i]]
        self.lefts = self.lefts[index:]

        self.__reset_iterator()

    def intersect_from_old(self, q:int):
        """
        crop this fat set to those elements satisfying >= q
        :param q:
        :return:
        """
        done = False
        while len(self.states) > 0 and not done:
            (a,b) = self.states[0]
            if b < q:
                self.states.pop(0)
            else:
                self.states[0] = (max(a,q),b)
                done = True
        self.__reset_iterator()

    def copy(self):
        """
        create and return a copy of this fat set
        the state of the iterator is not copied!
        :return:
        """
        copy = FatStateSet()
        copy.lefts = self.lefts.copy()
        copy.rights = self.rights.copy()
        return copy

    def __iter__(self):
        self.last_iterate = -1
        self.current_interval = 0
        return self

    def __next__(self):
        found = False
        while self.current_interval < len(self.lefts) and not found:
            a = self.lefts[self.current_interval]
            b = self.rights[a]
            if self.last_iterate == b:
                self.current_interval += 1
            else:
                if self.last_iterate >= a-1:
                    self.last_iterate += 1
                    found = True
                else:
                    self.last_iterate = a
                    found = True
        if found:
            return self.last_iterate
        else:
            raise StopIteration


class WorkList:

    worklist = {}

    def __init__(self):
        self.worklist = {}

    def is_empty(self):
        return len(self.worklist) == 0

    def add_pair(self, p:int, q:int):
        #(p,q) = (min(p,q), max(p,q))
        old_p = p
        p = min(p,q)
        q = max(old_p,q)
        if p in self.worklist:
            partners = self.worklist[p]
            partners.add_state(q)
            self.worklist[p] = partners
        else:
            partners = FatStateSet()
            partners.add_state(q)
            self.worklist[p] = partners

    def add_range(self, p:int, q:int, r:int):
        if p in self.worklist:
            partners = self.worklist[p]
            partners.add_states(q,r)
            self.worklist[p] = partners
        else:
            partners = FatStateSet()
            partners.add_states(q,r)
            self.worklist[p] = partners

    def take_next_pair(self):
        keys_iterator = iter(self.worklist)

        a = next(keys_iterator,None)
        if a != None:
            partners = self.worklist[a]
            b = partners.extract_min()
            if b == None:
                return None
            else:
                if partners.is_empty():
                    self.worklist.pop(a)
                return (a,b)
        return None
