#The following Python files are required to run the evaluations: apq.py, graph.py, evaluation.py
from apq import *

class Vertex:
    """ A Vertex in a graph. """
    
    def __init__(self, element):
        """ Create a vertex, with data element. """
        self._element = element

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def element(self):
        """ Return the data for the vertex. """
        return self._element
    
    def __lt__(self, v):
        """ Return true if this object is less than v.
       
        Args:
            v -- a vertex object
        """
        return self._element < v.element()

class Edge:
    """ An edge in a graph.

    Implemented with an order, so can be used for directed or undirected
    graphs. Methods are provided for both. It is the job of the Graph class
    to handle them as directed or undirected.
    """
    
    def __init__(self, v, w, weight, element):
        """ Create an edge between vertices v and w, with label element.

        Args:
            v -- a Vertex object
            w -- a Vertex object
            element -- the label, can be an arbitrarily complex structure.
        """
        self._vertices = (v,w)
        self._weight = weight
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                   + str(self._vertices[1]) + ' : '
                   + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge."""
        return self._vertices

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge, or None if this edge not incident on v.  
        
        Args:
            v - a Vertex object
        """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered pair. """
        return self._vertices[1]
    
    def weight(self):
        """ Return the weight of the edge. """
        return self._weight


class Graph:
    """ Represent a simple graph.

        This version maintains only undirected graphs, and assumes no
        self edges (i.e. no edge from a vertex v to v).
    """

    #Implement as a Python dictionary
    #  - the keys are the vertices
    #  - the values are the edge sets for that vertex
    #         Each edge set is also maintained as a dictionary,
    #         with opposite vertex as the key and the edge object as the value
    #         Suppose v and w are vertices in the graph, with an edge e between v and w
    #         self._structure[v] is a dictionary of edges
    #         self._structure[v][w] is the edge e
    
    def __init__(self):
        """ Create an initial empty graph. """
        self._structure = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + ' '
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    #--------------------------------------------------#
    #ADT methods to query the graph
    
    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])    #the dict of edges for v
        return num //2     #divide by 2, since each edge appears in the
                           #vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ get the first vertex that matches element. 
        
        BEWARE! - this method is inefficient, and will be really slow
        if used repeatedly on large graphs.
        """
        for v in self._structure:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                #to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v.

        Args:
            v -- a vertex object
        """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None, if there is no edge.

        Args:
            v -- a Vertex object
            w -- a Vertex object
        """
        if (self._structure != None
                         and v in self._structure
                         and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the degree of vertex v. 

        Args:
            v -- a Vertex object
        """
        return len(self._structure[v])

    #--------------------------------------------------#
    #ADT methods to modify the graph
    
    def add_vertex(self, element):
        """ Add and return a new vertex with data element.

        Note -- if there is already a vertex with the same data element,
        this will create another vertex instance with the same element.
        If the client using this ADT implementation does not want these 
        duplicates, it is the client's responsibility not to add duplicates.
        """
        v = Vertex(element)
        self._structure[v] = dict()  # create an empty dict, ready for edges
        return v

    def add_vertex_if_new(self, element):
        """ Add and return a vertex with element, if not already in graph.

        Checks for equality between the elements. If there is special
        meaning to parts of the element (e.g. element is a tuple, with an
        'id' in cell 0), then this method may create multiple vertices with
        the same 'id' if any other parts of element are different.

        To ensure vertices are unique for individual parts of element,
        separate methods need to be written.

        BEWARE! -- this uses linear search and will be inefficient for large graphs.
        """
        for v in self._structure:
            if v.element() == element:
                #print('Already in graph')
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, weight, element):
        """ Add and return an edge, with element, between two vertices v and w.

        If either v or w are not vertices in the graph, does not add, and
        returns None.
            
        If an edge already exists between v and w, this will
        replace the previous edge.

        Args:
            v -- a Vertex object
            w -- a Vertex object
            element -- arbitrary complex structure with info for the edge
        """
        if not v in self._structure or not w in self._structure:
            return None
        e = Edge(v, w, weight, element)
        # self._structure[v] is the dictionary of v's edges
        # so need to insert an entry for key w, with value e
        # A clearer way of expressing it would be
        # v_edges = self._structure[v]
        # v_edges[w] = e
        # etc.
        self._structure[v][w] = e  
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ Add all vertex triples in elist (v, w, weight) as edges with empty elements. """
        for (v,w,weight) in elist:
            self.add_edge(v,w,weight,None)

    #Additional methods to explore the graph
        
    def highestdegreevertex(self):
        """ Return the vertex with highest degree. """
        hd = -1
        hdv = None
        for v in self._structure:
            if self.degree(v) > hd:
                hd = self.degree(v)
                hdv = v
        return hdv            

    
    #Dijkstra implementations

    def dijkstra_heap_v1(self, src, dest):
        open = HeapAPQ()
        closed = {}
        locs = {}
        preds = {src: None}

        locs[src] = open.add(0, src)
        
        while open.length() > 0:
            vcost, v = open.remove_min()

            pred = preds.pop(v)
            locs.pop(v)
            
            closed[v] = (vcost, pred)

            for e in self.get_edges(v):
                w = e.opposite(v)
                if w not in closed:
                    newcost = vcost + e.weight()
                    if w not in locs:
                        preds[w] = v
                        locs[w] = open.add(newcost, w)
                    elif newcost < locs[w].key():
                        preds[w] = v
                        open.update_key(locs[w], newcost)
        
        return closed

    #Adapted to break out of the loop and return closed if the node removed from the heap is the destination
    def dijkstra_heap_v2(self, src, dest):
        open = HeapAPQ()
        closed = {}
        locs = {}
        preds = {src: None}

        locs[src] = open.add(0, src)
        
        while open.length() > 0:
            vcost, v = open.remove_min()

            pred = preds.pop(v)
            locs.pop(v)
            
            closed[v] = (vcost, pred)

            if v is dest:
                return closed

            for e in self.get_edges(v):
                w = e.opposite(v)
                if w not in closed:
                    newcost = vcost + e.weight()
                    if w not in locs:
                        preds[w] = v
                        locs[w] = open.add(newcost, w)
                    elif newcost < locs[w].key():
                        preds[w] = v
                        open.update_key(locs[w], newcost)
        
        return closed

    #Same as dijkstra_heap_v1, except ListAPQ is used instead of HeapAPQ    
    def dijkstra_list(self, src, dest):
        open = ListAPQ()
        closed = {}
        locs = {}
        preds = {src: None}

        locs[src] = open.add(0, src)
        
        while open.length() > 0:
            vcost, v = open.remove_min()

            pred = preds.pop(v)
            locs.pop(v)
            
            closed[v] = (vcost, pred)

            for e in self.get_edges(v):
                w = e.opposite(v)
                if w not in closed:
                    newcost = vcost + e.weight()
                    if w not in locs:
                        preds[w] = v
                        locs[w] = open.add(newcost, w)
                    elif newcost < locs[w].key():
                        preds[w] = v
                        open.update_key(locs[w], newcost)
        
        return closed
    
    #Q6 - Simpler Priority Queue
    def dijkstra_heap_q6(self, src, dest):
        open = HeapAPQ()
        closed = {}

        open.add(0, (src, None))
        
        while open.length() > 0:
            vcost, (v, pred) = open.remove_min()

            if v not in closed:
                closed[v] = (vcost, pred)

                for e in self.get_edges(v):
                    w = e.opposite(v)
                    if w not in closed:
                        newcost = vcost + e.weight()
                        open.add(newcost, (w, v))
        
        return closed