# linestorect

Discover rectangular in many lines

## Motivation

Given many lines, the task to discover those of them that form a rectangular is
well defined and quite easy to implement. But it is not trivial. In particular
not so, when a close approximation of rectangular is acceptable and even
required. To my surprise, when I was confronted by this task and looked for
existing solutions, I found none. Back then, I wrote code of my own. And now
time came to pay the technical debt and wrap that old code into a respectable
package. The current version works only for precise rectangulars. And I plan to
do so for approximations too.

## Usage

Install:

```shell
pip install linestorect
```

Use from code:

```python
from rect import Line, Rect, rects

lines = [
    Line((0, 0), (0, 1)),
    Line((0, 1), (1, 1)),
    Line((1, 1), (1, 0)),
    Line((1, 0), (0, 0)),
]

res = rects(*lines)

expected = Rect(a=(0, 0), b=(1, 0), c=(1, 1), d=(0, 1))

assert res == [expected]
```
