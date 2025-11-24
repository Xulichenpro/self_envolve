import os
import json
import logging

import llm
import tree
import utils
from prompts.self_envolve_prompt import self_envolve_user_prompt,self_envolve_system_prompt,diagnose_user_prompt

def self_envolve(agent_name:str):
    challenge_path = os.path.join(os.getcwd(),"ctf_crypto/challenge.json")
    with open(challenge_path,'r') as f:
        challenge = json.load(f)
    
    code = utils.get_patched_code(agent_name)

    if code == "success":
        return True
    elif code == "fail":
        return False

    log_path = os.path.join(os.getcwd(), agent_name,agent_name+".log")
    with open(log_path,'r') as f:
        log = f.read()

    msg = diagnose_user_prompt.format(challenge = challenge, runtime_log = log, code = code) + self_envolve_user_prompt
    response:str = llm.get_response_with_tools(self_envolve_system_prompt,msg,llm.process_tool(),logging.getLogger(agent_name))[-1]
    response = response["content"].split("\n")
    patch = ""
    flag = False
    for s in response:
        if "<patch>" in s.lower():
            if not flag:
                flag = True
                continue
        elif "patch>" in s.lower():
            break
        if flag:
            patch += s
            patch += '\n'
    patch = utils.clean_patch(patch)
    node = tree.nodes.query(agent_name)
    new_agent_name = utils.get_agent_name()
    os.makedirs(new_agent_name, exist_ok=True)
    tree.nodes.insert(new_agent_name,node.id)
    patch_path = os.path.join(os.getcwd(),new_agent_name,"patch.diff")
    with open(patch_path,"w") as f:
        f.write(patch)
    return False
    