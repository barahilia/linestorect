#!/usr/bin/env python
from rect import Line, rects


def demonstrate():
    lines = [
        Line((0, 0), (0, 1)),
        Line((0, 1), (1, 1)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (0, 0)),
    ]
    res = rects(*lines)
    print(res)


def demonstrate2():
    lines = [
        Line((0, 0), (0, 1)),
        Line((0, 1), (1, 1)),
        Line((1, 1), (1, 0)),
        Line((1, 0), (0, 0)),
    ]
    junk = [
        Line((i, 15), (i + 1, 15))
        for i in range(96)
    ]
    lines += junk
    print('And now we have %d distinct lines)' % len(set(lines)))
    res = rects(*lines)
    print(res)


if __name__ == '__main__':
    demonstrate()
    demonstrate2()
