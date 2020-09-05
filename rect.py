from collections import namedtuple, defaultdict
from tetragon import tetragon


Line = namedtuple('Line', ['a', 'b'])
Rect = namedtuple('Rect', ['a', 'b', 'c', 'd'])


def at_right_angle(a, b, c):
    assert a != b and b != c

    xa, ya = a
    xb, yb = b
    xc, yc = c

    x1 = xa - xb
    y1 = ya - yb

    x2 = xc - xb
    y2 = yc - yb

    inner_product = x1 * x2 + y1 * y2

    return inner_product == 0


def _make_graph(lines):
    graph = defaultdict(list)

    for line in lines:
        assert line.a != line.b

        graph[line.a].append(line)
        graph[line.b].append(line)

    return graph


def _get_cycle(lines):
    graph = _make_graph(lines)

    edge = lines[0]
    vertex = edge.a
    visited = set()

    while edge not in visited:
        yield vertex

        visited.add(edge)
        assert len(visited) <= len(lines)

        edges = graph[vertex]

        if len(edges) != 2:
            return

        assert edge in edges
        next_edge = edges[1] if edge == edges[0] else edges[0]

        assert vertex in [next_edge.a, next_edge.b]
        next_vertex = next_edge.b if vertex == next_edge.a else next_edge.a

        vertex, edge = next_vertex, next_edge

    yield vertex


def get_cycle(*lines):
    if not lines:
        return None

    vertexes = list(_get_cycle(lines))

    if len(vertexes) == len(lines) + 1:
        if vertexes[0] == vertexes[-1]:
            return vertexes[:-1]

    return None


def _get_rect(lines):
    assert len(lines) == 4

    cycle = get_cycle(*lines)

    if cycle is None:
        return None

    a, b, c, d = cycle

    all_right_angle = (
        at_right_angle(a, b, c) and
        at_right_angle(b, c, d) and
        at_right_angle(c, d, a) and
        at_right_angle(d, a, b)
    )

    if all_right_angle:
        return Rect(*cycle)

    return None


def _make_graph_points(lines):
    graph = defaultdict(set)

    for line in lines:
        assert line.a != line.b

        graph[line.a].add(line.b)
        graph[line.b].add(line.a)

    return graph


def _rects(lines):
    graph = _make_graph_points(lines)

    for quadro in tetragon(graph):
        a, b, c, d = quadro
        quadro = Line(a, b), Line(b, c), Line(c, d), Line(d, a)

        rect = _get_rect(quadro)

        if rect is not None:
            yield rect


def rects(*lines):
    return list(_rects(lines))
