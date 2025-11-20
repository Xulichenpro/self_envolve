import os
import json
import logging

import llm
from prompts.ctf_agent_prompt import system_prompt,user_prompt

def solve_ctf():
    challenge_path = os.path.join(os.getcwd(),"ctf_crypto/challenge.json")
    with open(challenge_path,'r') as f:
        challenge = json.load(f)
    msg = user_prompt.format(challenge=challenge)
    tools = llm.process_tool()

    from datetime import datetime

    now = datetime.now()  # 当前本地时间

    # 格式化
    formatted = now.strftime("%Y%m%d%H%M%S")
    print(formatted)


    # 1. 创建Logger
    logger = logging.getLogger("my_logger" + formatted)
    logger.setLevel(logging.DEBUG)  # 设置最低日志级别

    # 2. 创建Handler（文件输出）
    file_handler = logging.FileHandler("ctf_agent"+ formatted +"log")
    file_handler.setLevel(logging.DEBUG)

    # 3. 创建Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 4. 给Logger添加Handler
    logger.addHandler(file_handler)
    llm.get_response_with_tools(system_prompt,msg,tools,logger)

if __name__ == "__main__":
    solve_ctf()