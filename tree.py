from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    id:int
    name:str
    parent:int

class Tree:
    def __init__(self):
        self.tree:List[Node] = []

    def insert(self,agent_name:str,parent:int = -1):
        id = len(self.tree)
        node = Node(id,agent_name,parent)
        self.tree.append(node)

    def query(self,agent_name:str) -> Node:
        for node in self.tree:
            if node.name == agent_name:
                return node
        return None


nodes = Tree()
