class Graph:
    def __init__(self):
        self.vertices = {}
        self.number_of_vertices = 0

    def add_vertex(self, key):
        vertex = Vertex(key)
        self.vertices[key] = vertex
        self.number_of_vertices += 1

        return vertex

    def remove_vertex(self, key):
        return self.vertices.pop(key, None)

    def add_vertices(self, words):
        added = []
        from IPython import embed

        for word in words:
            sorted_word = ''.join(sorted(word))

            if sorted_word not in words:
                print "Appending: " + sorted_word
                added.append(self.add_vertex(sorted_word))

        return added

    def get_vertex(self, vertex):
        if vertex in self.vertices:
            return self.vertices[n]
        else:
            return None

    def add_edge(self,f,t,cost=0):
        if f not in self.vertices:
            nv = self.add_vertex(f)
        if t not in self.vertices:
            nv = self.add_vertex(t)

        self.vertices[f].add_neighbor(self.vertices[t], cost)

    def get_vertex_keys(self):
        return self.vertices.keys()

    def __iter__(self):
        return iter(self.vertices.values())


class Vertex:
    def __init__(self, word):
        self.word = word
        self.neighbors = {}

    def add_neighbor(self, neighbor, weight = 0):
        self.neighbors[neighbor] = weight
        return neighbor

    def get_neighbors(self):
        return self.neighbors.keys()
