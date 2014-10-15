from itertools import groupby
from collections import Counter
import graph as g
import random
import threading
import pickle


class WordList(object):
    def __init__(self, word_list):
        self.graph = g.Graph()
        self.words = [line.strip() for line in open(word_list)]
        self.partitioned = self.partition()

    def partition(self):
        groups = []
        unique_keys = []
        keyfunc = lambda s: len(s)
        data = sorted(self.words, key = keyfunc)

        for k, g in groupby(data, keyfunc):
            group = list(g)
            vertices = self.graph.add_vertices(group)
            groups.append(vertices)
            unique_keys.append(k)

        return {'groups': groups, 'unique_keys': unique_keys}

    def words_with_length(self, size):
        return self.partitioned['groups'][size - 2]


def dfs(vertex):
    stack = []
    visited = []
    stack.append(vertex)

    while len(stack) != 0:
        current_vertex = stack.pop()

        if current_vertex not in visited:
            visited.append(current_vertex)

            for neighbor in current_vertex.get_neighbors():
                if neighbor not in visited:
                    stack.append(neighbor)

    return visited


def get_chains(word_list):
    for root in word_list.words_with_length(2):
        visited = dfs(root)
        print "Length: " + str(len(visited))

        for node in visited:
            print "->" + node.word


def main():
    word_list = WordList('wordlist.txt')

    groups = word_list.partitioned['groups']
    f = open('word_list.pickle', 'w')


    for i in range(2, len(groups) + 1):
        print "Parent length: " + str(i)
        for parent in word_list.words_with_length(i):
            for child in word_list.words_with_length(i+1):
                if parent.word in child.word:
                    word_list.graph.add_edge(parent, child)

    pickle.dump(word_list, f)


if __name__ == "__main__":
    main()


