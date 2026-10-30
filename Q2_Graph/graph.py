"""
Generic unweighted directed graph.
Vertices can be any hashable value (e.g. strings), so this class contains
no course-specific code and can be reused in other projects.
"""
from collections import deque


class Graph:
    """Unweighted directed graph stored as adjacency sets in both directions."""

    def __init__(self):
        self._outgoing = {}  # vertex -> set of vertices it points TO
        self._incoming = {}  # vertex -> set of vertices pointing INTO it

    def _check(self, vertex):
        """Raise an error if the vertex is not in the graph."""
        if vertex not in self._outgoing:
            raise KeyError(f"Vertex {vertex!r} does not exist")

    # ---------- required methods ----------

    def addVertex(self, vertex):
        """Add a new vertex. Returns False if it already exists."""
        if vertex in self._outgoing:
            return False
        self._outgoing[vertex] = set()
        self._incoming[vertex] = set()
        return True

    def addEdge(self, from_vertex, to_vertex):
        """Add a directed edge from_vertex -> to_vertex. Returns False if it already exists."""
        self._check(from_vertex)
        self._check(to_vertex)
        if to_vertex in self._outgoing[from_vertex]:
            return False
        self._outgoing[from_vertex].add(to_vertex)
        self._incoming[to_vertex].add(from_vertex)  # keep the reverse index in sync
        return True

    def listIncomingAdjacentVertex(self, vertex):
        """Return all vertices that have an edge pointing INTO this vertex."""
        self._check(vertex)
        return list(self._incoming[vertex])

    # ---------- extra methods ----------

    def listOutgoingAdjacentVertex(self, vertex):
        """Return all vertices this vertex has an edge pointing TO."""
        self._check(vertex)
        return list(self._outgoing[vertex])

    def removeEdge(self, from_vertex, to_vertex):
        """Remove the edge from_vertex -> to_vertex. Returns False if it did not exist."""
        self._check(from_vertex)
        self._check(to_vertex)
        if to_vertex not in self._outgoing[from_vertex]:
            return False
        self._outgoing[from_vertex].remove(to_vertex)
        self._incoming[to_vertex].remove(from_vertex)
        return True

    def hasVertex(self, vertex):
        return vertex in self._outgoing

    def hasEdge(self, from_vertex, to_vertex):
        return from_vertex in self._outgoing and to_vertex in self._outgoing[from_vertex]

    def hasPath(self, start, goal):
        """Return True if goal can be reached from start by following edges (BFS)."""
        self._check(start)
        self._check(goal)
        visited = {start}
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            if vertex == goal:
                return True
            for neighbour in self._outgoing[vertex]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return False

    def getVertices(self):
        return list(self._outgoing)

    def __len__(self):
        return len(self._outgoing)