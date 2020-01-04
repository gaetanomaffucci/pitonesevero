from math import ceil

class BTreeNode(object):
    """A B-Tree Node.

    attributes
    =====================
    leaf : boolean, determines whether this node is a leaf
    keys : list, a list of keys internal to this node
    c : list, a list of children of this node
    """
    def __init__(self, leaf=False):
        self.leaf = leaf             #boolean is leaf
        self.keys = []                  #keys are keys[m-1]
        self.c = []                     #c
        self.parent = None
    #TODO change behavior of leaf

    def isleaf(self):
        if len(self.c)==0:
            return True
        else :
            return False

class BTree(object):
    def __init__(self, t):
        self.root = BTreeNode(leaf=True)
        # t is the minimum number of child that a node may have
        self.t = t

    """def insert(self, k):
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
    """

    def insert_key(self, key, x):
        x.keys.append(key)
        x.keys.sort()

    def node_full(self, x):
        if len(x.keys) > (2*self.t - 1):
            return True
        else:
            return False

    def split(self, x):
        i = ceil(len(x.keys)/2) - 1

        #case root without children
        if x.parent == None and len(x.c)==0:
            y = BTreeNode(leaf=True)
            y.keys = x.keys[0:i]
            y.parent = x
            z = BTreeNode(leaf=True)
            z.keys = x.keys[(i+1):len(x.keys)]
            z.parent = x
            temp = x.keys[i]
            x.keys.clear()
            x.keys.append(temp)
            x.c.append(y)
            x.c.append(z)
            x.leaf = False

        #root with children
        elif x.parent==None and len(x.c) > 0:
            y = BTreeNode()
            y.keys = x.keys[0:i]
            z = BTreeNode()
            z.keys = x.keys[(i+1):len(x.keys)]
            temp = x.keys[i]
            y.c = x.c[0:(i+1)]
            #for i in range (0,len(y.c)):

            z.c = x.c[(i+1):len(x.keys)+1]
            x.keys.clear()
            x.keys.append(temp)
            y.parent = x
            z.parent = x
            x.c.clear()
            x.c.append(y)
            x.c.append(z)
            x.leaf = False

        #Since overflow occurred in x we must split x
        else:

            print("AAA"+str(x.parent.keys))
            z = BTreeNode(leaf=True)
            self.insert_key(x.keys[i], x.parent)
            z.keys = x.keys[(i+1):len(x.keys)]
            x.keys = x.keys[0:i]
            x.parent.c.append(z)
            z.parent = x.parent
            if self.node_full(x.parent):
                self.split(x.parent)

        """if x.parent != None:
            self.insert_key(key, x)
            i = ceil(len(x.keys)/2) - 1
            z = BTreeNode(leaf=True)
            temp = x.keys[i]
            z.keys = x.keys[(i+1):len(x.keys)]
            x.keys = x.keys[0:i]
            x.parent.c.append(z)
            z.parent = x.parent
            x.parent.leaf = False
            x.parent.keys.append(temp)
        else:
            self.insert_key(key, x)
            y = BTreeNode(leaf=True)
            i = ceil(len(x.keys)/2) - 1
            y.keys = x.keys[0:i]
            y.parent = x
            z = BTreeNode(leaf=True)
            z.keys = x.keys[(i+1):len(x.keys)]
            z.parent = x
            temp = x.keys[i]
            x.keys.clear()
            x.keys.append(temp)
            x.c.append(y)
            x.c.append(z)
            x.leaf = False
        """


    def insert(self, key):
        x = self.insert_node(self.root, key)
        # if node x isn't full
        self.insert_key(key, x)
        if self.node_full(x):
            self.split(x)



    #return the node where the key should be inserted
    def insert_node(self, x, key):
        if x.leaf:
            return x
        else:
            for i in range(0, len(x.keys)):
                if key < x.keys[i]:
                    return self.insert_node(x.c[i], key)
                    break
            return self.insert_node(x.c[i+1], key)

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
                return x, i
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
            self.delete(pred)

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

    def print_node(self, x):
        #print("Level"+str(n)+":")
        print(x.keys)
        if not x.leaf:
            for i in range (0, len(x.keys) + 1):
                self.print_node(x.c[i])



#test
b = BTree(2)

for i in range (1,13):
    b.insert(i)


b.print_node(b.root)