# pylama: ignore=D100
import json
from algencode import Node, NumberNode
from rich import print

obj = {"op": "add", "args": [1, 2]}

n = Node(root=NumberNode(op="add", args=[1, 2]))

print(n)
print(n.model_dump())
print(Node.model_validate(n.model_dump()))
# print(Node.model_validate(json.dumps(obj)))
print(NumberNode.model_validate(json.dumps(obj)))
NumberNode.model_validate_json
