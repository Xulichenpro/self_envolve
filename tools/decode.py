import codecs

def decode(input:str,encoding:str)->str:
    return codecs.decode(input,encoding)

def discription() -> dict:
    tool = {
        "type": "function",
        "function": {
            "name": "decode",
            "description": "help decode an object",
            "parameters": {
                "type": "object",
                "properties": {
                    "input": {
                        "type": "string",
                        "description": "the object to be decoded"
                    },
                    "encoding": {
                        "type": "string",
                        "description": "the way you think the input is encoded, such as utf-8,rot_13,ascii,hex_codec,base64"
                    }
                },
                "required": ["input","encoding"]
            }
        }   
    }
    return tool

def tool_call(input:str,encoding:str):
    return decode(input,encoding)


