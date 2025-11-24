import os
import time
import shutil
import tempfile
import subprocess
from typing import List

import tree

def get_agent_name() -> str:
    current_time = str(int(time.time()))
    return "ctf_agent" + current_time

def copy_file(files:List[str],target:str):
    cwd = os.getcwd()
    dst_dir = os.path.join(cwd,target)
    os.makedirs(dst_dir, exist_ok=True)
    for f in files:
        shutil.copy2(f, dst_dir)

def clean_patch(raw_patch: str) -> str:
    lines = raw_patch.splitlines()
    start = None

    for i, line in enumerate(lines):
        if line.startswith("diff --git"):
            start = i
            break

    if start is None:
        raise ValueError("Invalid patch: no diff header found")

    return "\n".join(lines[start:]) + "\n"


def get_patched_code(agent_name:str):
    node = tree.nodes.query(agent_name)
    code = ""

    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(".", f"{tmp}/repo", dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git'))
        repo = f"{tmp}/repo"
        
        patches = []
        while node.parent != -1 :
            patches.append(repo + "/" + agent_name + "/patch.diff")
            node = tree.nodes.tree[node.parent]
        patches.reverse()

        # apply patch inside temp repo
        for patch in patches:
            check = subprocess.run(
                    ["git", "apply", "--check", patch],
                    cwd=repo,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)

            if check.returncode != 0:
                return "fail"
            subprocess.run(["git", "apply","--reject" ,patch], cwd=repo, check=True)

        eval_commands = ["python","ctf_agent.py", "-n",agent_name]
        res = subprocess.run(eval_commands,cwd=repo,capture_output=True,text=True)
        print(res)
        res = res.stdout.split("\n")

        for line in res:
            if "status" in line and "success" in line:
                shutil.copytree(repo, "final", dirs_exist_ok=True, ignore=shutil.ignore_patterns('.git'))
                return "success"
        
        copy_file([repo + "/" + agent_name + ".log"],agent_name)
        # read modified files (example: read all .py)
        for root, dirs, files in os.walk(repo):
            for fn in files:
                if fn.endswith(".py"):
                    path = os.path.join(root, fn)
                    with open(path, encoding="utf-8") as f:                       
                        code += f"----- {path} -----"
                        code += f.read()
        return code
