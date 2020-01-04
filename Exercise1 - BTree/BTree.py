from tree import Tree
from bisect import *

class BTree(Tree):
    #--------------------------------Node Class------------------------------------
    class _Node:
        __slots__ = '_parent', '_keys_', '_children'

        def __init__(self, parent=None):
          self._parent = parent
          self._keys = []
          self._children = []

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
        """Return the root Position of the alberi (or None if tree is empty)."""
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
        """Return the Position of p's left child (or None if no left child)."""
        node = self._validate(p)
        for child in node._children:
            yield self._make_position(child)

    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        return len(node._children)

    def _isleaf(self, p):
        """Return True if node is external, False if it's internal"""
        node = self._validate(p)
        return len(node._children)==0

    def _isnodefull(self,p):
        """Return True if the node is full, False otherwise"""
        node = self._validate(p)
        return len(node._keys) >= (2 * self._degree - 1)


    """Search for the position that contains the key"""
    def search_from_position(self, key, p = None):
        if p is None:
            node = self.root()
        else:
            node = self._validate(p)

        i = bisect_left(node._keys, key)
        if i!=len(node._keys) and node._keys[i] == key:
            return p
        elif self._isleaf(p):
            raise ValueError
        else:
            self.search_from_position(self, node._children[i-1], key)

    def _search_insert_position(self, key, node=None):
        if node is None:
            node = self._root
        i = bisect_left(node._keys, key)
        if i!=len(node._keys) and node._keys[i] == key:
            raise ValueError('Key already present')
        elif self._isleaf(self._make_position(node)):
            return self._make_position(node),i
        else:
            return self._search_insert_from_node(self, node.num_children(i-1), key)

    def insert(self, key):
        (p, i)=self._search_insert_position(key)
        node = self._validate(p)
        node._keys.insert(i, key)



if __name__=='__main__':
    b=BTree(2)
    print(len(b))