from rect import Line, Rect, rects, at_right_angle, get_cycle


def _standard_rect(r):
    return min(
        # forward: a -> b -> c -> d
        (r.a, r.b, r.c, r.d),
        (r.d, r.a, r.b, r.c),
        (r.c, r.d, r.a, r.b),
        (r.b, r.c, r.d, r.a),

        # opposite: d -> c -> b -> a
        (r.d, r.c, r.b, r.a),
        (r.a, r.d, r.c, r.b),
        (r.b, r.a, r.d, r.c),
        (r.c, r.b, r.a, r.d),
    )


def verify(lines, expected):
    result = rects(*lines)

    result = map(_standard_rect, result)
    expected = map(_standard_rect, expected)

    return set(result) == set(expected)


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
