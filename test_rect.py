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

    assert set(result) == set(expected)


def _point(s):
    return tuple(map(int, s))


def _points(s):
    return list(map(_point, s.split('-')))


def _line(s):
    return Line(*_points(s))


def _lines(s):
    return map(_line, s.split())


def _rect(s):
    return Rect(*_points(s))


def _rects(s):
    return map(_rect, s.split())


def test_interface():
    assert rects() == []


def test_unit_square():
    verify(
        _lines('00-01 01-11 11-10 10-00'),
        _rects('00-01-11-10')
    )


def test_gap():
    assert rects(*_lines('00-02 01-11 11-10 10-00')) == []
    assert rects(*_lines('00-01 01-12 11-10 10-00')) == []
    assert rects(*_lines('00-01 01-11 11-10 10-02')) == []


def test_right_angle():
    assert at_right_angle(*_points('10-00-01'))
    assert at_right_angle(*_points('50-10-11'))
    assert at_right_angle(*_points('33-13-12'))
    assert at_right_angle(*_points('12-01-10'))

    assert not at_right_angle(*_points('11-00-01'))
    assert not at_right_angle(*_points('20-11-12'))
    assert not at_right_angle(*_points('00-10-20'))


def test_non_right_angle():
    verify(
        _lines('00-02 02-11 11-10 10-00'),
        []
    )


def test_mixed_lines():
    verify(
        _lines('00-01 10-00 11-10 01-11'),
        _rects('00-01-11-10')
    )


def test_two_rects():
    verify(
        _lines('00-01 10-00 11-10 01-11 11-12 12-02 02-01'),
        _rects('00-01-11-10 01-11-12-02')
    )


def test_get_cycle():
    assert get_cycle(*_lines(
        '00-01 01-00')) == _points('00-01')

    assert get_cycle(*_lines(
        '00-01 01-02 02-03 03-04 04-00')) == _points('00-04-03-02-01')

    assert get_cycle(*_lines(
        '02-03 04-00 00-01 01-02 03-04')) == _points('02-01-00-04-03')

    assert get_cycle(*_lines(
        '03-02 04-00 00-01 02-01 03-04')) == _points('03-04-00-01-02')

    assert get_cycle(*_lines('00-01 01-02')) == None
    assert get_cycle(*_lines('00-01 01-00 01-00')) == None
    assert get_cycle(*_lines('00-01 00-10 00-11')) == None
    assert get_cycle(*_lines('00-01 01-00 02-03 03-02')) == None


def test_switched_line():
    verify(
        _lines('01-00 01-11 11-10 10-00'),
        _rects('00-01-11-10')
    )


def test_three_hidden_rectangles():
    verify(
        _lines(
            '00-01 01-11 11-10 10-00 ' +
            '20-21 21-31 31-30 30-20 ' +
            '44-55 55-73 73-62 62-44'
        ),
        _rects('00-01-11-10 20-21-31-30 44-55-73-62')
    )

    verify(
        _lines(
            '61-52 73-62 44-55 01-62 ' +
            '10-21 31-30 11-10 10-00 ' +
            '62-44 20-21 01-11 03-07 ' +
            '00-01 30-20 55-73 21-31'
        ),
        _rects('00-01-11-10 20-21-31-30 44-55-73-62')
    )
