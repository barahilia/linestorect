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


def _get_rect(cycle):
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
        rect = _get_rect(quadro)

        if rect is not None:
            yield rect


def rects(*lines):
    return list(_rects(lines))
