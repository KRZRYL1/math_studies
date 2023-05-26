from PriorityQueue import AdaptableHeapPriorityQueue

# ZADANIE 1

class Graph:
    class Vertex:
        """Reprezentacja wierzchołka w grafie"""
        __slots__ = '_element'

        def __init__(self, x):
            """Nie będziemy bezpośrednio wywoływać tej funkcji,
            tylko przy użyciu metody insert_vertex(x) klasy Graph"""
            self._element = x

        def element(self):
            """Zwracamy element powiązany z wierzchołkiem"""
            return self._element

        def __hash__(self):
            return hash(id(self))

    class Edge:
        """Reprezentacja krawędzi grafu"""
        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, u, v, x):
            """Nie będziemy wywoływać bezpośrednio"""
            self._origin = u
            self._destination = v
            self._element = x

        def endpoints(self):
            """Zwracamy krotkę (u,v) dla wierzchołków u i v."""
            return (self._origin, self._destination)

        def opposite(self, v):
            """Zwracamy wierzchołek na przeciw v jeśli istnieje"""
            return self._destination if v is self._origin else self._origin

        def element(self):
            """Zwracamy element powiązany z krawędzią"""
            return self._element

        def __hash__(self):
            return hash((self._origin, self._destination))


    def __init__(self, directed = False):
        """Tworzymy pusty graf, domyślnie niezorientowany"""
        self._outgoing = { }
        self._incoming = { } if directed else self._outgoing

    def is_directed(self):
        """Zwraca True jeśli graf jest zorientowany, bazując
        na początkowej deklaracji grafu"""
        return self._incoming is not self._outgoing

    def vertex_count(self):
        """Zwraca liczbę wierchołków"""
        return len(self._outgoing)

    def vertices(self):     #getVertices
        """Zwraca iterację wszystkich wierzchołków grafu"""
        return self._outgoing.keys()

    def edge_count(self):
        """Zwraca ilość krawędzi w grafie"""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        #w przypadku grafów niezorientowanych dzielimy przez 2 by uniknąć powtórzeń
        return total if self.is_directed() else total // 2

    def edges(self):    #getEdges
        """Zwraca 'set' wszystkich krawędzi grafu"""
        result = set()  # unikamy podwójnego zapisywania krawędzi dla grafu niezorientowanego
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())   #dodajemy krawędzie
        return result

    def get_edge(self,u,v):
        """Zwraca krawędź od u do v, None jeśli nie ma"""
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        """Zwraca ilość krawędzi wychodzących"""
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """Zwraca krawędzie wyjściowe"""
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None):    #addVertex
        """Dodaje i zwraca nowy wierchołek z elementem x"""
        v = self.Vertex(x)
        self._outgoing[v] = { }
        if self.is_directed():
            self._incoming[v] = { }
        return v

    def getVertex(self, n):
        """znajduje wierzchołek o podanym kluczu"""
        if n in self._outgoing:
            return self._outgoing[n]
        else:
            return None

    def insert_edge(self, u, v, x=None):  #addEdge dwie wersje w 1
        """Dodaje i zwraca nową krawędź od u do v"""
        e = self.Edge(u,v,x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e

    def __contains__(self, item):   #in
        return item in self._outgoing

    def to_dot(self):
        dot_str = "graph G {\n"
        for edge in self.edges():
            dot_str += '\t"{}" -> "{}";\n'.format(edge[0],edge[1])
        dot_str += "}"
        return dot_str


# ZADANIE 3

def BFS(g,s,discovered):
    """Breadth-First Search"""
    level = [s]                             # na początku tylko s
    while len(level)>0:
        next_level = []                     # tu zbieramy nowe wierchołki
        for u in level:
            for e in g.incident_edges(u):   # dla każdej krawędzi z u
                v = e.opposite(u)
                if v not in discovered:     # v jest nieodwiedzonym wierchołkiem
                    discovered[v] = e       # e to drzewo krawędzi, które 'odkryły' v
                    next_level.append(v)    # v będzie dalej rozpatrywane
        level = next_level                  # zamiana next na obecny i kontynuacja


def DFS(g, u, discovered):
    """Depth-First Search"""
    for e in g.incident_edges(u):           # dla każdej krawędzi z u
        v = e.opposite(u)
        if v not in discovered:             # v to nieodwiedzony wierzchołek
            discovered[v] = e               # e to drzewo krawędzi które 'odkryły' v
            DFS(g, v, discovered)           # odkrywamy od v dalej



# ZADANIE 4

def construct_path(u,v,discovered):
    path = []                               # domyślnie pusta ścieżka
    if v in discovered:                     # zbudowana lista od v do u i odwrócona na końcu
        path.append(v)
        walk = v
        while walk is not u:
            e = discovered[walk]            # krawędź prowadząca
            parent = e.opposite(walk)
            path.append(parent)
            walk = parent
        path.reverse()                      # reorientacja ścieżki od u do v
    return path

def DFS_complete(g):
    """Zwracamy 'forest' jako słownik"""
    forest = {}
    for u in g.vertices():
        if u not in forest:
            forest[u] = None                # u będzie korzeniem drzewa
            DFS(g,u,forest)
    return forest


# ZADANIE 5

def Dijkstra(g, src):
    d = {}
    cloud = {}
    pq = AdaptableHeapPriorityQueue()
    pqlocator = {}

    for v in g.vertices():
        if v is src:
            d[v] = 0
        else:
            d[v] = float('inf')
        pqlocator[v] = pq.add(d[v],v)

    while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u] = key
        del pqlocator[u]
        for e in g.incident_edges(u):
            v = e.opposite(u)
            if v not in cloud:
                wgt = e.element()
                if d[u] + wgt < d[v]:
                    d[v] = d[u] + wgt
                    pq.update(pqlocator[v], d[v], v)
    return cloud

def shortest_path_tree(g,s,d):
    tree = {}
    for v in d:
        if v is not s:
            for e in g.incident_edges(v, False):
                u = e.opposite(v)
                wgt = e.element()
                if d[v] == d[u]+wgt:
                    tree[v] = e
    return tree


g = Graph()
for i in range(6):
    g.insert_vertex(i)
print(g)