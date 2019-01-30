from rect import Line, Rect, rects, at_right_angle, is_rect, is_polyline, \
    is_cycle, get_cycle


def test_interface():
    assert rects() == []


def test_unit_square():
    assert rects(
        Line((0, 0), (0, 1)),
        Line((0, 1), (1, 1)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (0, 0))
    ) == [
        Rect(
            (0, 0),
            (0, 1),
            (1, 1),
            (1, 0)
        )
    ]


def test_gap():
    assert rects(
        Line((0, 0), (0, 0)),
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


def test_right_angle():
    assert rects(
        Line((0, 0), (0, 2)),
        Line((0, 2), (1, 1)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (0, 0))
    ) == []


def test_mixed_lines():
    assert rects(
        Line((0, 0), (0, 1)),
        Line((1, 0), (0, 0)),
        Line((1, 1), (1, 0)),
        Line((0, 1), (1, 1)),
    ) == [
        Rect(
            (0, 0),
            (0, 1),
            (1, 1),
            (1, 0)
        )
    ]


def test_two_rects():
    assert rects(
        Line((0, 0), (0, 1)),
        Line((1, 0), (0, 0)),
        Line((1, 1), (1, 0)),
        Line((0, 1), (1, 1)),

        Line((1, 1), (1, 2)),
        Line((1, 2), (0, 2)),
        Line((0, 2), (0, 1)),
    ) == [
        Rect((0, 0), (0, 1), (1, 1), (1, 0)),
        Rect((0, 1), (1, 1), (1, 2), (0, 2)),
    ]


def test_has_four_edges():
    line = Line((0, 0), (0, 1))
    edges_count = [0, 1, 2, 3, 5, 6]

    for count in edges_count:
        assert not is_rect([line] * count)

    assert is_rect([
        Line((0, 1), (0, 0)),
        Line((0, 1), (1, 1)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (0, 0)),
    ])


def test_has_four_vertices():
    line = Line((0, 0), (0, 1))
    assert not is_rect([line] * 4)

    assert not is_rect([
        Line((0, 1), (0, 0)),
        Line((0, 1), (1, 1)),
        Line((0, 1), (0, 0)),
        Line((0, 1), (1, 1)),
    ])

    assert is_rect([
        Line((0, 1), (0, 0)),
        Line((0, 1), (1, 1)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (0, 0)),
    ])


def test_is_polyline():
    assert is_polyline(
        Line((0, 0), (0, 1)),
    )
    assert is_polyline(
        Line((0, 0), (0, 1)),
        Line((0, 1), (2, 1)),
    )
    assert is_polyline(
        Line((0, 0), (0, 1)),
        Line((0, 1), (2, 1)),
        Line((2, 1), (3, 4)),
        Line((3, 4), (1, 5)),
    )

    assert not is_polyline(
        Line((0, 0), (0, 0)),
    )
    assert not is_polyline(
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 0)),
    )
    assert not is_polyline(
        Line((0, 0), (0, 1)),
        Line((0, 0), (0, 2)),
        Line((0, 0), (0, 3)),
    )


def test_mixed_polyline():
    assert is_polyline(
        Line((0, 0), (0, 1)),
        Line((2, 1), (0, 1)),
    )
    assert is_polyline(
        Line((0, 0), (0, 1)),
        Line((0, 0), (2, 1)),
    )


def test_is_cycle():
    assert is_cycle(
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 0)),
    )
    assert is_cycle(
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 2)),
        Line((0, 2), (0, 3)),
        Line((0, 3), (0, 4)),
        Line((0, 4), (0, 0)),
    )
    assert is_cycle(
        Line((0, 2), (0, 3)),
        Line((0, 4), (0, 0)),
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 2)),
        Line((0, 3), (0, 4)),
    )
    assert is_cycle(
        Line((0, 3), (0, 2)),
        Line((0, 4), (0, 0)),
        Line((0, 0), (0, 1)),
        Line((0, 2), (0, 1)),
        Line((0, 3), (0, 4)),
    )

    assert not is_cycle(
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 2)),
    )
    assert not is_cycle(
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 0)),
        Line((0, 1), (0, 0)),
    )
    assert not is_cycle(
        Line((0, 0), (0, 1)),
        Line((0, 1), (0, 0)),

        Line((0, 2), (0, 3)),
        Line((0, 3), (0, 2)),
    )


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


def xtest_switched_line():
    assert rects(
        Line((0, 1), (0, 0)),
        Line((0, 1), (1, 1)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (0, 0)),
    ) == [
        Rect((0, 0), (0, 1), (1, 1), (1, 0))
    ]
