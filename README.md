algencode
=========

Small library for encoding and decodable runnable instructions as JSON.

```python
s = """
{
    "op": "mul",
    "args": [
        {
            "op": "add",
            "args": [1, {"key": "a"}, {"key": "b"}],
        },
        2,
    ],
}
"""

n = Node.parse_raw(s)

assert n.reduce({"a": 2, "b": 3}) == 12
assert n.reduce({"a": 24, "b": 25}) == 100
```

Todo
----

- [ ] Add `float` to `LiteralNode`
