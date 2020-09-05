from collections import defaultdict
from tetragon import tetragon


def make_bigraph(graph):
    res = defaultdict(list)

    for a in graph:
        for b in graph[a]:
            res[a].append(b)
            res[b].append(a)

    return res


def test_simplest():
    graph = {0: [1, 2], 1: [3], 2: [3]}
    assert [(0, 1, 3, 2)] == list(tetragon(graph))


def test_two_from_same_origin():
    graph = {
        0: [1, 2, 3, 4],
        1: [5], 2: [5],
        3: [6], 4: [6],
    }
    assert [
        (0, 1, 5, 2),
        (0, 3, 6, 4),
    ] == list(tetragon(graph))


def test_single_in_bigraph():
    graph = {0: [1, 2], 1: [3], 2: [3]}
    bigraph = make_bigraph(graph)

    assert {
        (0, 1, 3, 2),
        (1, 0, 2, 3),
        (2, 0, 1, 3),
        (3, 1, 0, 2),
    } == set(tetragon(bigraph))
