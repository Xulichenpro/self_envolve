import os
import json
import logging
import argparse

import llm
import tree
from prompts.ctf_agent_prompt import system_prompt,user_prompt

def solve_ctf(agent_name:str):
    challenge_path = os.path.join(os.getcwd(),"ctf_crypto/challenge.json")
    with open(challenge_path,'r') as f:
        challenge = json.load(f)
    msg = user_prompt.format(challenge=challenge)
    tools = llm.process_tool()

    # 1. 创建Logger
    logger = logging.getLogger(agent_name)
    logger.setLevel(logging.DEBUG)  # 设置最低日志级别

    # 2. 创建Handler（文件输出）
    cwd = os.getcwd()
    log_path = os.path.join(cwd, agent_name + ".log")
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)


    # 3. 创建Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 4. 给Logger添加Handler
    logger.addHandler(file_handler)
    llm.get_response_with_tools(system_prompt,msg,tools,logger)
    node = tree.nodes.query(agent_name)
    node.eval = True
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent_name","-n",required=True)

    args = parser.parse_args()
    solve_ctf(args.agent_name)