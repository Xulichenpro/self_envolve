import os
import shutil
import tempfile
import subprocess
from typing import List

import tree

def copy_folder(source:str,target:str):
    cwd = os.getcwd()
    src = os.path.join(cwd, source)
    dst = os.path.join(cwd, target, source)
    shutil.copytree(src, dst, dirs_exist_ok=True)

def copy_file(files:List[str],target:str):
    cwd = os.getcwd()
    dst_dir = os.path.join(cwd,target)
    os.makedirs(dst_dir, exist_ok=True)
    for f in files:
        shutil.copy2(os.path.join(cwd, f), dst_dir)

def get_patched_code(agent_name:str):
    node = tree.nodes.query(agent_name)
    patches = []
    while node.parent != -1 :
        patches.append(agent_name + "/patch.diff")
        node = tree.nodes[node.parent]
    patches.reverse()

    code = ""
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(".", f"{tmp}/repo", dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git'))
        repo = f"{tmp}/repo"

        # apply patch inside temp repo
        for patch in patches:
            subprocess.run(["git", "apply", patch], cwd=repo, check=True)

        # read modified files (example: read all .py)
        for root, dirs, files in os.walk(repo):
            for fn in files:
                if fn.endswith(".py"):
                    path = os.path.join(root, fn)
                    with open(path, encoding="utf-8") as f:                       
                        code += f"----- {path} -----"
                        code += f.read()
        return code
