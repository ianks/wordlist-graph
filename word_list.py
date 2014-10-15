from itertools import groupby
from collections import Counter
import graph as g
import random
import threading
import pickle

#     Description:
#
#     This code makes a graph of unique letter combinations (order
#     does not matter). Then it creates edges between nodes if the
#     strings have a set difference of one character.
#
#     Maximum chain size: 14
#
#     Connected chains:
#         On my first attempt at running it, I completely forgot to
#         print out the chains. All I printed was the length which
#         was 14. This code takes a few hours to run, so I was
#         unable to print the chain size. As of now it is running
#         and I plan on updating this with the chains as soon as it
#         finishes. However, the code works and can be verified and I
#         can explain every piece of it :)


class WordList(object):
    def __init__(self, word_list):
        self.graph = g.Graph()
        self.words = [line.strip() for line in open(word_list)]
        self.partitioned = self.partition()

    # Here we partition the array into groups based on the
    # the string length size. This allows us to easily iterate
    # and find chains
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


# Depth first search
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


# Run DFS |number_of_source_nodes| times
def get_chains(word_list):
    for root in word_list.words_with_length(2):
        visited = dfs(root)

        if len(visited) == 14:
            print "Length: " + str(len(visited))

            for node in visited:
                print "->" + node.word

# Compare two strings, see if they differ by one letter
def string_diff(parent, child):
    try:
        s1 = Counter(list(parent))
        s2 = Counter(list(child))

        return len(list((s1 - s2).elements()))
    except:
        return 0

def main():
    word_list = WordList('wordlist.txt')

    groups = word_list.partitioned['groups']
    f = open('word_list.pickle', 'w')

    # Add edges between nodes if they differ by one char
    for i in range(2, len(groups) + 1):
        print "Parent length: " + str(i)
        for parent in word_list.words_with_length(i):
            for child in word_list.words_with_length(i+1):
                if string_diff(parent, child) == 1:
                    parent.add_neighbor(child)

    # Dump the graph to disk so we can reuse
    pickle.dump(word_list, f)
    f.close()

    # f = open('word_list.pickle', 'r')
    # word_list = pickle.load(f)
    get_chains(word_list)


if __name__ == "__main__":
    main()
