class BTreeNode(object):
    """A B-Tree Node.

    attributes
    =====================
    leaf : boolean, determines whether this node is a leaf
    keys : list, a list of keys internal to this node
    c : list, a list of children of this node
    """
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.c    = []
        self.parent = None

class BTree(object):
    def __init__(self, t):
        self.root = BTreeNode(leaf=True)
        # t is the minimum number of child that a node may have
        self.t = t

    def insert(self, k):
        r = self.root
        if len(r.keys) == (2*self.t) - 1:     # keys are full, so we must split
            s = BTreeNode()
            self.root = s
            s.c.insert(0, r)                  # former root is now 0th child of new root s
            self._split_child(s, 0)
            self._insert_nonfull(s, k)
        else:
            self._insert_nonfull(r, k)

    def _insert_nonfull(self, x, k):
        i = len(x.keys) - 1     # i is the number of node's keys x subtracted of 1 because index go from 0
        if x.leaf:
            # if k isn't greater of those present (if it were, the while loop would not be run)
            # then it is need to see in which position of list "keys" insert k
            x.keys.append(0)
            while i >= 0 and k < x.keys[i]:
                x.keys[i+1] = x.keys[i]
                i -= 1
            # add key in the position i+1 of list "keys"
            x.keys[i+1] = k
        else:
            # insert a child
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.c[i].keys) == (2*self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_nonfull(x.c[i], k)

    def _split_child(self, x, i):
        t = self.t
        y = x.c[i]
        z = BTreeNode(leaf=y.leaf)

        # slide all children of x to the right and insert z at i+1.
        x.c.insert(i+1, z)
        x.keys.insert(i, y.keys[t-1])

        # keys of z are t to 2t - 1,
        # y is then 0 to t-2
        z.keys = y.keys[t:(2*t - 1)]
        y.keys = y.keys[0:(t-1)]

        # children of z are t to 2t els of y.c
        if not y.leaf:
            z.c = y.c[t:(2*t)]
            y.c = y.c[0:(t-1)]

    def search(self, k, x):
        """Search the B-Tree for the key k.

        args
        =====================
        k : Key to search for
        x : (optional) Node at which to begin search. Can be None, in which case the entire tree is searched.

        """
        if isinstance(x, BTreeNode):
            i = 0
            while i < len(x.keys) and k > x.keys[i]:    # look for index of k
                i += 1
            if i < len(x.keys) and k == x.keys[i]:      # found exact match
                return x,i
            elif x.leaf:                                # no match in keys, and is leaf ==> no match exists
                return None
            else:                                       # search children
                x.c[i].parent = x
                return self.search(k, x.c[i])
        else:                                           # no node provided, search root of tree
            return self.search(k, self.root)

    def delete(self, element):

        #search in which node and posizion in this is the element searched
        x,i = self.search(element, None)

        #CASE 1: node "x" is not leaf search predecessor of element
        if not x.leaf:
            #methos takes as parameters the node "x" and position "i"
            pred = self.predecessor(x, i)
            #in the position "i" of element in the node "x", we take the predecessor founded
            x.keys.insert(i, pred)

        #CASE 2: node "x" is leaf
        else:
            #CASE 2.1: the leaf contains >t-1 keys ---> can delete the element from node "x"
            if len(x.keys) > self.t - 1:
                x.keys.remove(element)
            #CASE 2.2: the leaf contains t-1 keys ---> in this case there are others two cases
            elif len(x.keys) == self.t - 1:
                # need to found index "j" that indicates the position of list c of node parent
                for j in range (0,len(x.parent.keys)+1):
                    if x.parent.c[j].keys[0] == x.keys[0]:
                        if j != 0:
                            k = j - 1
                        else:
                            k = j + 1
                        break
                #CASE 2.2.1: redistribute the keys with adjacent sibling
                # adjacent sibling is to left
                if len(x.parent.c[k].keys) > self.t - 1 and k == j - 1:
                    j = k
                    index = len(x.parent.c[k].keys) - 1
                    self.redistribution(element, k, j, index, x)
                # adjacent sibling is to right
                elif len(x.parent.c[k].keys) > self.t - 1 and k == j + 1:
                    index = 0
                    self.redistribution(element, k, j, index, x)
                #CASE 2.2.2: fusion with adjacent sibling
                # adjacent sibling is to left
                elif len(x.parent.c[k].keys) == self.t - 1 and k == j - 1:
                    self.fusion(element, x, k, j)
                # adjacent sibling is to right
                elif len(x.parent.c[k].keys) == self.t - 1 and k == j + 1:
                    self.fusion(element, x, j, k)

    def predecessor(self, x, i):
        j = len(x.c[i].keys)
        if x.c[i].leaf:
            temp = x.c[i].keys[j-1]
            x.c[i].keys.remove(temp)
            return temp
        else:
            self.predecessor(x.c[i], j+1)

    def fusion(self, element, x, k, j):
        x.parent.c[k].append(x.parent.keys[k])
        x.keys.remove(element)
        x.parent.c[k].keys.extend(x.parent.c[j].keys)
        x.parent.c[j].keys.clear()
        x.parent.keys.remove(x.parent.keys[k])

    def redistribution(self, element, k, j, index, x):
        temp = x.parent.keys[j]
        x.parent.keys.insert(j, x.parent.c[k].keys[index])
        x.parent.c[k].keys.remove(x.parent.c[k].keys[index])
        x.keys.append(temp)
        x.keys.remove(element)
        x.keys.sort()