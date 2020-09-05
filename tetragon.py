from itertools import combinations


def tetragon(graph):
    nodes = list(graph)

    for node in nodes:
        yield from _tetragon(graph, node)


def _tetragon(graph, a):
    seconds = graph[a]

    assert a not in seconds
    assert len(seconds) == len(set(seconds))

    for b, c in combinations(seconds, 2):
        assert a != b and a != c and b != c

        thirds = set(graph[b]) & set(graph[c])
        thirds -= {a, b, c}

        for d in thirds:
            # Note: d stands between b and c
            yield a, b, d, c
