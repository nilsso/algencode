# pylama: ignore=D100
from algencode import Node

procs = {
    "_wow": Node.parse_obj({"key": "wow"}),
}
n = Node.parse_obj({"proc": "_wow"})
vals = {
    "wow": 420,
}
print(n.reduce(vals, procs))
