import os
import json

import llm
import utils
from prompts.self_envolve_prompt import self_envolve_user_prompt,self_envolve_system_prompt,diagnose_user_prompt

def self_envolve(agent_name:str):
    challenge_path = os.path.join(os.getcwd(),"ctf_crypto/challenge.json")
    with open(challenge_path,'r') as f:
        challenge = json.load(f)
    log_path = os.path.join(os.getcwd(), agent_name, agent_name+".log")
    with open(log_path,'r') as f:
        log = json.load(f)
    
    code = utils.get_patched_code(agent_name)

    msg = diagnose_user_prompt.format(challenge = challenge, runtime_log = log, code = code) + self_envolve_user_prompt
    response:str = llm.get_response_with_tools(self_envolve_system_prompt,msg,tools = llm.process_tool())[-1]
    response = response.split("\n")
    patch = ""
    flag = False
    for s in response:
        if "<patch>" in s.lower():
            if not flag:
                flag = True
                continue
            else:
                break
        if flag:
            patch += s

    patch_path = os.join(os.getcwd(),agent_name,"patch.diff")
    with open(patch_path,"w") as f:
        f.write(patch)
    