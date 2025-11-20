import os
import json
import time
from pathlib import Path
import importlib.util
import logging

import openai
from typing import List

def create_client():
    return openai.OpenAI(base_url="https://api.deepseek.com/v1" ,\
                        api_key=os.getenv("DeepSeek_API_KEY"))

def get_response(system_msg:str , msg:str , msg_history:List[dict] = None , temperature:float = 0.7):
    if not msg_history:
        msg_history = []
    
    client = create_client()
    new_msg_history = msg_history + [{"role":"user","content":msg}]
    response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content":system_msg},
                *new_msg_history,
            ],
            temperature=temperature,
        )
    response = response.choices[0].message.content
    print(response)
    new_msg_history += [{"role":"assistant","content":response}]
    return new_msg_history

def process_tool() -> List[dict]:
    tools = []
    tools_dir = os.path.join(os.getcwd(), "tools")
    folder = Path(tools_dir)

    for py_file in folder.glob("*.py"):
        module_name = py_file.stem   # 文件名作为模块名，例如 a.py → a

        # 动态加载模块
        spec = importlib.util.spec_from_file_location(module_name, py_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 执行其中的函数discription()
        if hasattr(module, "discription"):
            result = module.discription()
            #print(py_file, "=>", result)
            tools.append(result)
    return tools

def get_response_with_tools(system_msg:str , msg:str , tools:List[dict], logger, msg_history:List[dict] = None , temperature:float = 0.7,max_time_out:int = 300,max_retry:int = 5):
    start_time = time.time()
    
    if not msg_history:
        msg_history = []
    
    client = create_client()
    logger.info("system prompt: " + system_msg)
    logger.info("user prompt: " + msg)
    new_msg_history = msg_history + [{"role":"user","content":msg}]
    while True:
        current_time = time.time()
        if current_time - start_time >= max_time_out:
            logger.error("time out!")
            if max_retry > 0 :
                logger.info("the agent will retry")
                return get_response_with_tools(system_msg,msg,tools,logger,msg_history = new_msg_history,temperature = temperature, max_time_out = max_time_out, max_retry = max_retry - 1)
            else :
                logger.info("fail to solve the problem")
            break
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content":system_msg},
                *new_msg_history,
            ],
            temperature=temperature,
            tools=tools
        )
    
        print(response)
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            new_msg_history += [{"role":"assistant",
                                 "content":None,
                                 "tool_calls": response.choices[0].message.tool_calls}]
            id = tool_call.id
            tool = tool_call.function.name
            args = tool_call.function.arguments
            logger.info("agent's thinking: " + response.choices[0].message.content)
            logger.info("tool call: \n" + "  tool name : " + tool + "\n  args :" + args)
            args = json.loads(args)
            spec = importlib.util.spec_from_file_location(tool, os.path.join(os.getcwd(),"tools",f"{tool}.py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "tool_call"):
                try:
                    result = module.tool_call(**args)
                except Exception as e:
                    logger.error(f"tool call error : {e}")
                    new_msg_history += [{"role":"tool",
                                      "tool_call_id": id,
                                      "content": e }]
                logger.info("tool result : " + str(result))
                new_msg_history += [{"role":"tool",
                                      "tool_call_id": id,
                                      "content": str(result) }]
        else:
            new_msg_history += [{"role":"assistant","content":response.choices[0].message.content}]
            logger.info("final result : " + response.choices[0].message.content)
            break
    return new_msg_history

if __name__ == "__main__":
    system_msg = "You are a helpful assistant good at solving ctf problems."
    msg = "here is a single problem: please decode : URYYB "
    tools = process_tool()
    #get_response_with_tools(system_msg,msg,tools)