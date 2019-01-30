from collections import namedtuple, defaultdict
from itertools import permutations


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


def _are_rect_lines(l1, l2):
    a, b = l1
    c, d = l2

    if a == b or c == d or b != c:
        return False

    return at_right_angle(a, b, d)


def get_rect(*lines):
    assert len(lines) == 4

    points = [line.a for line in lines]

    lines = lines + (lines[0],)

    rect_lines = all(
        _are_rect_lines(l1, l2)
        for l1, l2 in zip(lines[:-1], lines[1:])
    )

    if rect_lines:
        return Rect(*points)


def _rects(lines):
    for quadro in permutations(lines, 4):
        rect = get_rect(*quadro)

        if rect is not None:
            yield rect


def rects(*lines):
    out = set()

    for r in _rects(lines):
        again = (
            r in out or
            Rect(r.d, r.a, r.b, r.c) in out or
            Rect(r.c, r.d, r.a, r.b) in out or
            Rect(r.b, r.c, r.d, r.a) in out
        )

        if not again:
            out.add(r)

    return list(out)


def is_rect(lines):
    if len(lines) != 4:
        return False

    vertices = set(
        [line.a for line in lines] +
        [line.b for line in lines]
    )

    if len(vertices) != 4:
        return False

    return True


def is_polyline(*lines):
    if not lines:
        return False

    distinct = len(set(lines)) == len(lines)

    if not distinct:
        return False

    vertex_to_edges = defaultdict(list)

    for line in lines:
        fake_edge = line.a == line.b

        if fake_edge:
            return False

        vertex_to_edges[line.a].append(line)
        vertex_to_edges[line.b].append(line)

    ends = [
        vertex for vertex, lines in vertex_to_edges.items()
        if len(lines) == 1
    ]

    if len(ends) != 2:
        return False

    first_end, second_end = ends

    vertex = first_end
    checked_vertexes = {vertex}
    edge, = vertex_to_edges[first_end]

    while True:
        next_vertex = edge.b if edge.a == vertex else edge.a

        assert next_vertex not in checked_vertexes
        checked_vertexes.add(next_vertex)

        junction = vertex_to_edges[next_vertex]

        if len(junction) == 0:
            assert False
        elif len(junction) == 1:
            if checked_vertexes == set(vertex_to_edges):
                assert next_vertex == second_end
                return True
            else:
                return False
        elif len(junction) == 2:
            next_edge = junction[1] if junction[0] == edge else junction[0]
            vertex, edge = next_vertex, next_edge
        else:
            assert len(junction) > 3
            return False


def _are_distinct_lines(lines):
    return (
        lines and
        len(set(lines)) == len(lines) and
        all(line.a != line.b for line in lines)
    )


def _make_graph(lines):
    graph = defaultdict(list)

    for line in lines:
        assert line.a != line.b

        graph[line.a].append(line)
        graph[line.b].append(line)

    return graph


def is_cycle(*lines):
    if not _are_distinct_lines(lines):
        return False

    graph = _make_graph(lines)

    edge = lines[0]
    vertex = edge.a
    visited = set()

    while edge not in visited:
        visited.add(edge)

        edges = graph[vertex]

        if len(edges) != 2:
            return False

        assert edge in edges
        next_edge = edges[1] if edge == edges[0] else edges[0]

        assert vertex in [next_edge.a, next_edge.b]
        next_vertex = next_edge.b if vertex == next_edge.a else next_edge.a

        vertex, edge = next_vertex, next_edge

    assert len(visited) <= len(lines)
    return len(visited) == len(lines)


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
