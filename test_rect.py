from rect import Line, Rect, rects, at_right_angle, get_cycle


def same_rect(r, q):
    return r in [
        # forward: a -> b -> c -> d
        Rect(q.a, q.b, q.c, q.d),
        Rect(q.d, q.a, q.b, q.c),
        Rect(q.c, q.d, q.a, q.b),
        Rect(q.b, q.c, q.d, q.a),

        # opposite: d -> c -> b -> a
        Rect(q.d, q.c, q.b, q.a),
        Rect(q.a, q.d, q.c, q.b),
        Rect(q.b, q.a, q.d, q.c),
        Rect(q.c, q.b, q.a, q.d),
    ]


def verify(lines, expected):
    res = rects(*lines)

    if len(res) != len(expected):
        assert False

    for r, q in zip(res, expected):
        assert same_rect(r, q)


def test_interface():
    assert rects() == []


def test_unit_square():
    verify([
        Line((0, 0), (0, 1)),
        Line((0, 1), (1, 1)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (0, 0))
    ],
    [
        Rect(
            (0, 0),
            (0, 1),
            (1, 1),
            (1, 0)
        )
    ])


def test_gap():
    assert rects(
        Line((0, 0), (0, 2)),
        Line((0, 1), (1, 1)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (0, 0))
    ) == []

    assert rects(
        Line((0, 0), (0, 1)),
        Line((0, 1), (1, 2)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (0, 0))
    ) == []

    assert rects(
        Line((0, 0), (0, 1)),
        Line((0, 1), (1, 1)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (2, 0))
    ) == []


def test_right_angle():
    assert at_right_angle((1, 0), (0, 0), (0, 1)) == True
    assert at_right_angle((5, 0), (1, 0), (1, 1)) == True
    assert at_right_angle((0, 0), (1, 0), (1, -1)) == True
    assert at_right_angle((1, 2), (0, 1), (1, 0)) == True

    assert at_right_angle((1, 1), (0, 0), (0, 1)) == False
    assert at_right_angle((2, 0), (1, 1), (1, 2)) == False
    assert at_right_angle((0, 0), (1, 0), (2, 0)) == False


def test_non_right_angle():
    assert rects(
        Line((0, 0), (0, 2)),
        Line((0, 2), (1, 1)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (0, 0))
    ) == []


def test_mixed_lines():
    verify([
        Line((0, 0), (0, 1)),
        Line((1, 0), (0, 0)),
        Line((1, 1), (1, 0)),
        Line((0, 1), (1, 1)),
    ],
    [
        Rect(
            (0, 0),
            (0, 1),
            (1, 1),
            (1, 0)
        )
    ])


def test_two_rects():
    verify([
        Line((0, 0), (0, 1)),
        Line((1, 0), (0, 0)),
        Line((1, 1), (1, 0)),
        Line((0, 1), (1, 1)),

        Line((1, 1), (1, 2)),
        Line((1, 2), (0, 2)),
        Line((0, 2), (0, 1)),
    ], [
        Rect((0, 0), (0, 1), (1, 1), (1, 0)),
        Rect((0, 1), (1, 1), (1, 2), (0, 2)),
    ])


def test_get_cycle():
    assert get_cycle(
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 0)),
    ) == [(0, 0), (0, 1)]

    assert get_cycle(
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 2)),
        Line((0, 2), (0, 3)),
        Line((0, 3), (0, 4)),
        Line((0, 4), (0, 0)),
    ) == [(0, 0), (0, 4), (0, 3), (0, 2), (0, 1)]

    assert get_cycle(
        Line((0, 2), (0, 3)),
        Line((0, 4), (0, 0)),
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 2)),
        Line((0, 3), (0, 4)),
    ) == [(0, 2), (0, 1), (0, 0), (0, 4), (0, 3)]

    assert get_cycle(
        Line((0, 3), (0, 2)),
        Line((0, 4), (0, 0)),
        Line((0, 0), (0, 1)),
        Line((0, 2), (0, 1)),
        Line((0, 3), (0, 4)),
    ) == [(0, 3), (0, 4), (0, 0), (0, 1), (0, 2)]

    assert get_cycle(
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 2)),
    ) == None

    assert get_cycle(
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 0)),
        Line((0, 1), (0, 0)),
    ) == None

    assert get_cycle(
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 0)),

        Line((0, 2), (0, 3)),
        Line((0, 3), (0, 2)),
    ) == None


def test_switched_line():
    verify([
        Line((0, 1), (0, 0)),
        Line((0, 1), (1, 1)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (0, 0)),
    ], [
        Rect((0, 0), (0, 1), (1, 1), (1, 0))
    ])
