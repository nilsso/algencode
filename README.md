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

assert n.reduce({"a": 2, "b": 3}) == 12  # 2*(1+2+3) == 12 ✅
assert n.reduce({"a": 24, "b": 25}) == 100  # 2*(1+24+25) == 100 ✅
```

Node types
----------

### Numeric node

Keyword | Description
--- | ---
`"op"` | Operation to perform
`"args"` | A sequence of nodes that *must* reduce to numeric nodes, or a variable node that points to such a sequence.

#### Supported operations

- `"add"`
- `"sub"`
- `"mul"`
- `"mod"`
- `"div"`
- `"min"`
- `"max"`
- `"round"`
- `"len"`
- `"mean"`

Todo
----

- [ ] Add some `float` tests
- [ ] Add some `Decimal` tests
- [ ] Add some `date` tests
- [ ] Add some `ProcNode` tests
