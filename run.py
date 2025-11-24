import random
import shutil

import utils
import tree
import envolve

def initialize_run():
    agent_name = utils.get_agent_name()
    tree.nodes.insert(agent_name)
    shutil.copytree(".", agent_name, dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git'))

def main():
    initialize_run()
    while True:
        id = random.randint(0,len(tree.nodes.tree) - 1)
        node:tree.Node = tree.nodes.tree[id]
        flag = envolve.self_envolve(node.name)
        if flag:
            break

if __name__ == "__main__":
    main()


