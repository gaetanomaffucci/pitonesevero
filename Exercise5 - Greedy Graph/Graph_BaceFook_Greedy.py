# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#    Data Structures and Algorithms in Python
#    Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#    John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#from DataStructure.priority_queue.adaptable_heap_priority_queue import *

class Graph:
  """Representation of a simple graph using an adjacency map."""

  #------------------------- nested Vertex class -------------------------
  class Vertex:
    """Lightweight vertex structure for a graph."""
    __slots__ = '_element', '_visited', '_color', '_signed'

    def __init__(self, x):
      """Do not call constructor directly. Use Graph's insert_vertex(x)."""
      self._element = x
      self._visited = False
      self._color = False
      self._signed = False

    def element(self):
      """Return element associated with this vertex."""
      return self._element

    def __hash__(self):         # will allow vertex to be a map/set key
      return hash(id(self))

    def __str__(self):
      return str(self._element)

  #------------------------- nested Edge class -------------------------
  class Edge:
    """Lightweight edge structure for a graph."""
    __slots__ = '_origin', '_destination', '_element'

    def __init__(self, u, v, x):
      """Do not call constructor directly. Use Graph's insert_edge(u,v,x)."""
      self._origin = u
      self._destination = v
      self._element = x

    def endpoints(self):
      """Return (u,v) tuple for vertices u and v."""
      return (self._origin, self._destination)

    def opposite(self, v):
      """Return the vertex that is opposite v on this edge."""
      if not isinstance(v, Graph.Vertex):
        raise TypeError('v must be a Vertex')
      if v is self._origin:
        return self._destination
      elif v is self._destination:
          return self._origin
      raise ValueError('v not incident to edge')

    def element(self):
      """Return element associated with this edge."""
      return self._element

    def __hash__(self):         # will allow edge to be a map/set key
      return hash( (self._origin, self._destination) )

    def __str__(self):
      return '({0},{1},{2})'.format(self._origin,self._destination,self._element)

  #------------------------- Graph methods -------------------------
  def __init__(self, directed=False):
    """Create an empty graph (undirected, by default).

    Graph is directed if optional paramter is set to True.
    """
    self._outgoing = {}
    # only create second map for directed graph; use alias for undirected
    self._incoming = {} if directed else self._outgoing
    self.list_vertex = []

  def _validate_vertex(self, v):
    """Verify that v is a Vertex of this graph."""
    if not isinstance(v, self.Vertex):
      raise TypeError('Vertex expected')
    if v not in self._outgoing:
      raise ValueError('Vertex does not belong to this graph.')

  def is_directed(self):
    """Return True if this is a directed graph; False if undirected.

    Property is based on the original declaration of the graph, not its contents.
    """
    return self._incoming is not self._outgoing # directed if maps are distinct

  def vertex_count(self):
    """Return the number of vertices in the graph."""
    return len(self._outgoing)

  def vertices(self):
    """Return an iteration of all vertices of the graph."""
    return self._outgoing.keys()

  def edge_count(self):
    """Return the number of edges in the graph."""
    total = sum(len(self._outgoing[v]) for v in self._outgoing)
    # for undirected graphs, make sure not to double-count edges
    return total if self.is_directed() else total // 2

  def edges(self):
    """Return a set of all edges of the graph."""
    result = set()       # avoid double-reporting edges of undirected graph
    for secondary_map in self._outgoing.values():
      result.update(secondary_map.values())    # add edges to resulting set
    return result

  def get_edge(self, u, v):
    """Return the edge from u to v, or None if not adjacent."""
    self._validate_vertex(u)
    self._validate_vertex(v)
    return self._outgoing[u].get(v)        # returns None if v not adjacent

  def degree(self, v, outgoing=True):
    """Return number of (outgoing) edges incident to vertex v in the graph.

    If graph is directed, optional parameter used to count incoming edges.
    """
    self._validate_vertex(v)
    adj = self._outgoing if outgoing else self._incoming
    return len(adj[v])

  def incident_edges(self, v, outgoing=True):
    """Return all (outgoing) edges incident to vertex v in the graph.

    If graph is directed, optional parameter used to request incoming edges.
    """
    self._validate_vertex(v)
    adj = self._outgoing if outgoing else self._incoming
    for edge in adj[v].values():
      yield edge

  def insert_vertex(self, x=None):
    """Insert and return a new Vertex with element x."""
    v = self.Vertex(x)
    self._outgoing[v] = {}
    if self.is_directed():
      self._incoming[v] = {}        # need distinct map for incoming edges
    return v

  def insert_edge(self, u, v, x=None):
    """Insert and return a new Edge from u to v with auxiliary element x.

    Raise a ValueError if u and v are not vertices of the graph.
    Raise a ValueError if u and v are already adjacent.
    """
    if self.get_edge(u, v) is not None:      # includes error checking
      raise ValueError('u and v are already adjacent')
    e = self.Edge(u, v, x)
    self._outgoing[u][v] = e
    self._incoming[v][u] = e

  """def create_queue(self):
      queue = AdaptableHeapPriorityQueue()
      for i in range (self.vertices()):
          queue.add(i, self.degree(i))
      return queue

  def function_min_user(self, queue):
      while queue.__len__() != 0:
          vertex, degree = queue.remove()
          for k in range (len(self.list_vertex_selected)):
              if not self.get_edge(vertex, self.list_vertex_selected[k]) == None:
                  break
              elif k == len(self.list_vertex_selected) - 1:
                self.list_vertex_selected.append(vertex)
          if len(self.list_vertex_selected) == 0:
              self.list_vertex_selected.append(vertex)
      return self.list_vertex_selected
  """

  def calculate_max(self):
      list = []
      for i in (self.vertices()):
          tuple = (self.degree(i), i)
          list.append(tuple)
      list.sort(key = lambda x : x[0])
      return list

  def function_min_user(self, vert):
      while len(vert) != 0:
          tuple = vert.pop()
          x = tuple[1]
          for k in range (len(self.list_vertex)):
              if not self.get_edge(x, self.list_vertex[k]) == None:
                  break
              elif k == len(self.list_vertex) - 1:
                self.list_vertex.append(x)
          if len(self.list_vertex) == 0:
              self.list_vertex.append(x)
      return self.list_vertex

#test
g = Graph()
vert = []
for i in range(17):
    vert.append(g.insert_vertex(i))

g.insert_edge(vert[0],vert[1])
g.insert_edge(vert[0],vert[2])
g.insert_edge(vert[0],vert[5])
g.insert_edge(vert[0],vert[3])

g.insert_edge(vert[0],vert[4])
g.insert_edge(vert[0],vert[6])
g.insert_edge(vert[0],vert[7])
g.insert_edge(vert[0],vert[8])
g.insert_edge(vert[0],vert[9])
g.insert_edge(vert[0],vert[10])
g.insert_edge(vert[0],vert[11])
g.insert_edge(vert[0],vert[12])
g.insert_edge(vert[0],vert[13])
g.insert_edge(vert[0],vert[14])
g.insert_edge(vert[0],vert[15])
g.insert_edge(vert[0],vert[16])

g.insert_edge(vert[1],vert[13])
g.insert_edge(vert[2],vert[4])
g.insert_edge(vert[2],vert[3])
g.insert_edge(vert[3],vert[12])
g.insert_edge(vert[3],vert[9])
g.insert_edge(vert[4],vert[6])
g.insert_edge(vert[5],vert[8])
g.insert_edge(vert[5],vert[7])
g.insert_edge(vert[7],vert[14])
g.insert_edge(vert[9],vert[10])
g.insert_edge(vert[9],vert[11])
g.insert_edge(vert[10],vert[15])

g.insert_edge(vert[6],vert[2])
g.insert_edge(vert[6],vert[10])
g.insert_edge(vert[6],vert[11])
g.insert_edge(vert[6],vert[15])

g.insert_edge(vert[11],vert[7])
g.insert_edge(vert[11],vert[14])
g.insert_edge(vert[11],vert[10])
g.insert_edge(vert[11],vert[3])
g.insert_edge(vert[11],vert[15])

list = g.calculate_max()
s = g.function_min_user(list)
for i in range(len(s)):
    print(s[i])

"""queue = g.create_queue()
s = g.function_min_user(queue)
for i in range(len(s)):
    print(s[i])"""
