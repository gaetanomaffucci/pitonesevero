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

    def getdegree(self):
        return self._t

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
            new_child._children = node._children[middle + 1:]
            # slice operator does not complain in case of empty children array

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

    # ---------------------------------------- delete utility methods ----------------------------------------
    """"Utility method for find the previous key in left sibling or its descendants"""
    def predecessor(self, node, index):
        if self.isleaf(self._make_position(node._children[index])):
            return node._children[index]
        else:
            j = len(node._children[index]._keys)
            return self.predecessor(node._children[index], j)

    def fusion(self, parent, left_node_index, right_node_index):
        left_node = parent._children[left_node_index]
        right_node = parent._children[right_node_index]

        left_node._keys.append(parent._keys[left_node_index])
        del parent._keys[left_node_index]

        left_node._keys.extend(right_node._keys)
        del parent._children[right_node_index]

    def undersize(self, node):
        if node._parent is not None:

            # need to find index of this node inside parent's children array
            last_key = node._keys[-1]

            parent_node = node._parent
            parent_keys = parent_node._keys
            node_index = bisect_left(parent_keys, last_key)

            # CASE 2.2.1: redistribute the keys with adjacent sibling
            # adjacent sibling is to left
            if node_index > 0:
                other_node=parent_node._children[node_index-1]
                if len(other_node._keys) > self._degree - 1:
                    self.redistribution(parent_node, node_index-1, node_index)
                else:
                    self.fusion(parent_node, node_index-1, node_index)
                if len(parent_keys) < self._degree - 1:
                    self.undersize(parent_node)

            #The node is the first, check for redistribution or fusion between node 0 and 1
            elif len(parent_node._children[1]._keys) > self._degree - 1:
                    self.redistribution(parent_node, 0, 1)
            else:
                    self.fusion(parent_node,0,1)


        #children of root have been fused together as we have checked before we have elements left in the tree
        elif len(node._keys) == 0:
            self._root = node._children[0]

    def redistribution(self, parent, left_node_index, right_node_index):
        left_node = parent._children[left_node_index]
        right_node = parent._children[right_node_index]

        if len(left_node._keys) > len(right_node._keys):
            last_child = left_node._children[-1]
            last_element = left_node._keys[-1]

            right_node._keys.insert(0, parent._keys[left_node_index])
            last_child._parent = right_node
            right_node._children.insert(0, last_child)

            parent._keys[left_node_index] = last_element

            del left_node._keys[-1]
            del left_node._children[-1]
        else:
            first_child = right_node._children[0]
            first_element = right_node._keys[0]

            left_node._keys.append(parent._keys[left_node_index])
            first_child._parent = left_node
            left_node._children.append(first_child)

            parent._keys[left_node_index] = first_element

            del right_node._keys[0]
            del right_node._children[0]

    # ---------------------------------------- delete methods ------------------------------------------------

    def delete(self, key):

        #Search the node where the key is (if present)
        (position, index) = self._search_from_position(key,self.root())

        node = self._validate(position)

        # If node is not leaf, swap with the previous element then delete from the leaf
        if not self.isleaf(position):

            temp = node._keys[index]

            # we find the previous key in the left sibling or one of its descendants
            predecessor = self.predecessor(node, index)

            #swap key and predecessor
            node._keys[index]=predecessor._keys[-1]
            predecessor._keys[-1]=temp

            #now we proceed with delete in the sibling or descendant of sibling
            node=predecessor
            index=len(node._keys)-1


        node._keys.remove(key)
        self._size -= 1

        # the leaf contains less than t-1 keys
        if len(node._keys) < self._degree - 1 and self._size > 0:
            self.undersize(node)
        elif self._size == 0:
            self._root = None



if __name__=='__main__':
    b=BTree(3)
    for i in range (1,24):
            b.insert(i)
    b.delete(23)
    b.delete(17)
    b.delete(11)
    b.print_from_position(b.root())







