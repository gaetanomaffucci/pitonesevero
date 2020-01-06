from tree import Tree
from bisect import bisect_left
from math import ceil
import logging

class BTree(Tree):
    # --------------------------------Node Class------------------------------------
    class _Node:

        def __init__(self, parent=None):
          self._parent = parent
          self._keys = []
          self._children = []

        def __str__(self):
            return str(self._keys)

        # -------------------------- nested Position class --------------------------

    class Position(Tree.Position):
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

        def __str__(self):
            return str(self._container)+str(self._node)
    # ------------------------------- methods -------------------------------

    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:  # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None

    def __init__(self,degree):
        """Create an initially empty BTree of given degree."""
        self._root = None
        self._degree = degree  # the minimum number of children for nodes except for the root
        self._size = 0

    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def root(self):
        """Return the root Position of the tree(or None if tree is empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return the Position of p's parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def keys(self, p):
        """Return the keys stored in the Position."""
        node= self._validate(p)
        for key in node._keys:
         yield key

    def children(self, p):
        """Return the Position of p's children (or None if has no  children)."""
        node = self._validate(p)
        for child in node._children:
            yield self._make_position(child)

    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        return len(node._children)

    def isleaf(self, p):
        """Return True if node contained in Position is external, False if it's internal"""
        node = self._validate(p)
        return len(node._children)==0

    def _isfull(self, p):
        """Return True if the node contained in Position is full, False otherwise"""
        node = self._validate(p)
        return len(node._keys) > (2 * self._degree - 1)

    # ---------------------------------------- search methods -----------------------------------------------------
    """Search for the position that contains the key"""
    def search(self, key):
        return self._search_from_position(key, self.root())[0]

    """Private method for search a key. Return a tuple with the position and the insertion index"""
    def _search_from_position(self, key, p):
        node = self._validate(p)


        i = bisect_left(node._keys, key)

        if i!=len(node._keys) and node._keys[i] == key:
            return (p,i)
        elif self.isleaf(p):
            raise ValueError
        else:
            return self._search_from_position(key, self._make_position(node._children[i]))

    """Search for the node which should contains the key"""
    def _search_insert_node(self, key, node=None):
        if node is None:
            node = self._root
        i = bisect_left(node._keys, key)

        if i!=len(node._keys) and node._keys[i] == key:
            raise ValueError('Key already present')
        elif self.isleaf(self._make_position(node)):
            return node,i
        else:
            return self._search_insert_node(key, node._children[i])

    # ---------------------------------------- insert method -----------------------------------------------------

    """Insert the key in the tree if not already present, otherwise raise a ValueError"""
    def insert(self, key):
        if(self._root == None):
            node = BTree._Node()
            node._keys.append(key)
            self._root = node
        else:
            (node, i)=self._search_insert_node(key)

            node._keys.insert(i, key)
            if self._isfull(self._make_position(node)):
                self._split(node)
        self._size += 1

    def _split(self, node):
        middle = ceil(len(node._keys)/2) - 1
        middle_key = node._keys[middle]



        #special case, node is root of tree
        if node._parent is None:
            new_root = BTree._Node()

            new_child = BTree._Node(new_root)
            new_child._keys = node._keys[middle + 1:]
            new_child._children = node._children[middle + 1:] # slice operator does not complain in case of empty children array

            for c in new_child._children:
                c._parent=new_child

            new_root._keys.append(middle_key)
            new_root._children.append(node)
            new_root._children.append(new_child)

            del node._keys[middle:]
            del node._children[middle + 1:]
            node._parent = new_root
            self._root = new_root

        else:
            parent_node=node._parent

            new_node = BTree._Node(parent_node)
            new_node._keys = node._keys[middle + 1:]
            new_node._children = node._children[middle + 1:]

            for c in new_node._children:
                c._parent = new_node

            del node._keys[middle:]
            del node._children[middle + 1:]

            parent_index=bisect_left(parent_node._keys,middle_key)

            parent_node._keys.insert(parent_index,middle_key)
            parent_node._children.insert(parent_index+1,new_node)

            if self._isfull(self._make_position(node._parent)):
                self._split(node._parent)

    """Utility function for print the tree (Warning: the result may not be very readable)"""
    def print_from_position(self, p):
        node=self._validate(p)
        print(node._keys)
        if not self.isleaf(p):
            for c in self.children(p):
                self.print_from_position(c)

    # ---------------------------------------- delete method -----------------------------------------------------
    def delete(self, key):

        #Search the node where the key is (if present)
        (position, index) = self._search_from_position(key,self.root())

        node = self._validate(position)

        # CASE 1: node "x" is not leaf search predecessor of element
        if not self.isleaf(position):
            # utility methods takes as parameters the position and position "i"
            pred = self.predecessor(x, i)
            # in the position "i" of element in the node "x", we take the predecessor found
            x.keys.insert(i, pred)
            self.delete(pred)

        # CASE 2: node "x" is leaf
        else:
            # CASE 2.1: the leaf contains >t-1 keys ---> can delete the element from node "x"
            if len(node._keys) > self.t - 1:
                node._keys.remove(key)
            # CASE 2.2: the leaf contains t-1 keys ---> in this case there are others two cases
            elif len(x.keys) == self.t - 1:
                # need to found index "j" that indicates the position of list c of node parent
                for j in range(0, len(x.parent.keys) + 1):
                    if x.parent.c[j].keys[0] == x.keys[0]:
                        if j != 0:
                            k = j - 1
                        else:
                            k = j + 1
                        break
                # CASE 2.2.1: redistribute the keys with adjacent sibling
                # adjacent sibling is to left
                if len(x.parent.c[k].keys) > self.t - 1 and k == j - 1:
                    j = k
                    index = len(x.parent.c[k].keys) - 1
                    self.redistribution(element, k, j, index, x)
                # adjacent sibling is to right
                elif len(x.parent.c[k].keys) > self.t - 1 and k == j + 1:
                    index = 0
                    self.redistribution(element, k, j, index, x)
                # CASE 2.2.2: fusion with adjacent sibling
                # adjacent sibling is to left
                elif len(x.parent.c[k].keys) == self.t - 1 and k == j - 1:
                    self.fusion(element, x, k, j)
                # adjacent sibling is to right
                elif len(x.parent.c[k].keys) == self.t - 1 and k == j + 1:
                    self.fusion(element, x, j, k)


if __name__=='__main__':
    b=BTree(6)
    for i in range (1,1000,5):
            b.insert(i)

    print(b.search(96))
    #b.print_from_position(b.root())






