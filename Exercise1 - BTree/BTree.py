from tree import Tree
from bisect import bisect_left
from math import ceil

class BTree(Tree):
    #--------------------------------Node Class------------------------------------
    class _Node:

        def __init__(self, parent=None):
          self._parent = parent
          self._keys = []
          self._children = []

        def __str__(self):
            return str(self._parent)+str(self._keys)+str(self._children)

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
        # ------------------------------- utility methods -------------------------------

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

    def _isfull(self,p):
        """Return True if the node contained in Position is full, False otherwise"""
        node = self._validate(p)
        return len(node._keys) >= (2 * self._degree - 1)

    """Search for the position that contains the key"""
    def search(self, key):
        return self._search_from_position(key, self.root())

    def _search_from_position(self, key, p):
        node = self._validate(p)


        i = bisect_left(node._keys, key)

        if i!=len(node._keys) and node._keys[i] == key:

            return p
        elif self._isleaf(p):
            raise ValueError
        else:
            return self._search_from_position(key, self._make_position(node._children[i]))

    """Search for the node which should contains the key"""
    def _search_insert_node(self, key, node=None, flag=False):
        if node is None:
            node = self._root
        i = bisect_left(node._keys, key)

        if i!=len(node._keys) and node._keys[i] == key:
            raise ValueError('Key already present')
        elif self.isleaf(self._make_position(node)):
            return node,i
        else:
            return self._search_insert_node(key, node._children[i])

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

    def _split(self, node):
        middle = ceil(len(node._keys)/2) - 1
        middle_key = node._keys[middle]



        #special case, node is root of tree
        if node._parent is None:
            new_root = BTree._Node()

            new_child = BTree._Node(new_root)
            new_child._keys = node._keys[middle + 1:]
            new_child._children = node._children[middle + 1:] # slice operator does not complain in case of empty children array

            new_root._keys.append(middle_key)
            new_root._children.append(node)
            new_root._children.append(new_child)

            del node._keys[middle:]
            del node._children[middle+1:]
            node._parent=new_root
            self._root=new_root

        else:

            new_node = BTree._Node(node._parent)
            new_node._keys = node._keys[middle + 1:]
            new_node._children = node._children[middle + 1:]

            del node._keys[middle:]
            del node._children[middle + 1:]

            parent_index=bisect_left(node._parent._keys,middle_key)

            node._parent._keys.insert(parent_index,middle_key)
            node._parent._children.insert(parent_index+1,new_node)

            if self._isfull(self._make_position(node._parent)):
                print("doppio split")
                self._split(node._parent)


    def _print_from_position(self, p):
        node=self._validate(p)
        print(node._keys)
        if not self.isleaf(p):
            for c in self.children(p):
                self._print_from_position(c)

if __name__=='__main__':
    b=BTree(2)
    for i in range (10,18):
        b.insert(i)
    """
    start = BTree._Node()
    start._keys = [12]
    left= BTree._Node(start)
    left._keys=[11]
    right=BTree._Node(start)
    right._keys=[13]
    start._children.append(left)
    start._children.append(right)
    b._root=start

    b.insert(14)
    b.insert(15)
    b.insert(9)
    b.insert(10)
    """
    b._print_from_position(b.root())
