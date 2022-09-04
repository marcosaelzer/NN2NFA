# class to represent sets of intervals of non-negative integers
# currently based on simple ordered lists
# TODO: change to balanced search-tree implementation

class FatStateSet:
    # a fat set is a list of non-negative integer pairs [(a_1,b_1),(a_2,b_2),...,(a_n,b_n)]
    # satisfying a_i <= b_i and b_i < a_(i+1)-1 for all i=1,..,n-1
    # and representing the set {a_1,..,b_1,a_2,..,b_2,...,a_n..,b_n}

    states = []

    def __init__(self):
        self.states = []
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
        return self.states == []

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
        for (a,b) in self.states:
            if not first:
                s += ","
            first = False
            if a == b:
                s += str(a)
            else:
                s += str(a) + ",..," + str(b)
        s += "}"
        return s

    def contains(self, q:int):
        """
        checks whether state q is contained in this fat set
        :param q:
        :return:
        """
        for (a,b) in self.states:
            if a <= q and q <= b:
                return True
        return False

    def add_state(self,q:int):
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

    def add_states(self, p:int, q:int):
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

    def remove_state(self,q:int):
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
        l = len(self.states)
        if l == 0:
            return None
        else:
            (_,b) = self.states[l-1]
            return b

    def extract_min(self):
        if len(self.states) == 0:
            return None
        else:
            (a,b) = self.states[0]
            if a==b:
                self.states.pop(0)
                return a
            else:
                self.states[0] = (a+1,b)
                return a

    def complement(self, n:int):
        """
        complements a fat set with respect to the set {0,...,n-1}
        :param n:
        :return:
        """
        comp = FatStateSet()

        l = len(self.states)
        m = n-1

        if l > 0:
            (_,b) = self.states[l-1]
            if b+1 <= m:
                comp.add_states(b+1,m)

        for i in range(l-2,-1,-1):
            (_,b) = self.states[i]
            (c,_) = self.states[i+1]
            if b+1 <= m:
                comp.add_states(b+1,min(c-1,m))

        if l > 0:
            (a,_) = self.states[0]
            if a > 0:
                comp.add_states(0,a-1)

        return comp

    def intersect_from(self, q:int):
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
        for i in range(len(self.states)-1,-1,-1):
            (a,b) = self.states[i]
            copy.add_states(a,b)
        return copy

    def __iter__(self):
        self.last_iterate = -1
        self.current_interval = 0
        return self

    def __next__(self):
        found = False
        while self.current_interval < len(self.states) and not found:
            (a,b) = self.states[self.current_interval]
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