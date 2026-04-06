import os
import re
import sys
from typing import List, Dict, Any, Optional
from llm_provider import LLMProvider
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from telemetry.logger import logger
class ReActAgent:
    """
    A ReAct-style Agent that follows the Thought-Action-Observation loop.
    """
    
    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def get_system_prompt(self) -> str:
        """
        System prompt that instructs the agent to follow ReAct strictly.
        """
        tool_descriptions = "\n".join([f"- {t['name']}: {t['description']}" for t in self.tools])
        return f"""
        You are an intelligent reasoning assistant. You must solve problems step-by-step using the ReAct framework.
        You have access to the following tools:
        {tool_descriptions}

        You MUST strictly use the following format for EVERY step:
        Thought: your detailed reasoning about what to do next.
        Action: tool_name(arguments_as_string)
        Observation: the result of the action (provided by the system, do not generate this yourself).
        ... (repeat Thought/Action/Observation until you have the final answer)
        Thought: I now know the final answer.
        Final Answer: your final response to the user.
        """

    def run(self, user_input: str) -> str:
        """
        The core ReAct loop: Generate -> Parse -> Execute -> Append -> Repeat.
        """
        logger.log_event("AGENT_START", {"input": user_input, "model": self.llm.model_name})
        
        # Scratchpad là nơi lưu trữ toàn bộ lịch sử Suy nghĩ - Hành động - Kết quả
        # LLM cần đọc lại cái này để biết bước tiếp theo phải làm gì.
        scratchpad = f"User Query: {user_input}\n"
        steps = 0

        while steps < self.max_steps:
            logger.log_event("AGENT_STEP", {"step": steps + 1, "max_steps": self.max_steps})
            
            # 1. Gọi LLM và đưa toàn bộ scratchpad vào
            try:
                response_data = self.llm.generate(prompt=scratchpad, system_prompt=self.get_system_prompt())
                llm_output = response_data.get("content", "")
            except Exception as e:
                logger.log_event("AGENT_ERROR", {"error": str(e)})
                return f"Lỗi khi gọi LLM: {str(e)}"
            
            # Ghi nhận output của LLM vào scratchpad
            scratchpad += f"{llm_output}\n"

            # 2. Kiểm tra xem LLM đã tìm ra Final Answer chưa
            # Sử dụng re.DOTALL để lấy toàn bộ chữ kể cả khi có dấu xuống dòng
            final_answer_match = re.search(r"Final Answer:\s*(.*)", llm_output, re.DOTALL | re.IGNORECASE)
            if final_answer_match:
                final_answer = final_answer_match.group(1).strip()
                logger.log_event("AGENT_END", {"steps": steps + 1, "status": "success", "answer": final_answer})
                return final_answer

            # 3. Parse Thought & Action
            # Tìm pattern: Action: ten_ham(tham_so)
            action_match = re.search(r"Action:\s*([a-zA-Z0-9_]+)\((.*?)\)", llm_output)
            
            if action_match:
                tool_name = action_match.group(1).strip()
                tool_args = action_match.group(2).strip()
                
                # 4. Thực thi Tool và nối Observation vào scratchpad
                observation = self._execute_tool(tool_name, tool_args)
                scratchpad += f"Observation: {observation}\n"
                
                logger.log_event("TOOL_EXECUTED", {
                    "tool": tool_name, 
                    "args": tool_args, 
                    "observation": observation
                })
            else:
                # Nếu LLM trả lời tào lao sai format, ép nó suy nghĩ lại
                error_msg = "Error - No valid Action or Final Answer format found. Please follow the strict format."
                scratchpad += f"Observation: {error_msg}\n"
                logger.log_event("AGENT_WARNING", {"warning": "LLM violated format constraints"})

            steps += 1
            
        logger.log_event("AGENT_END", {"steps": steps, "status": "max_steps_reached"})
        return "Agent stopped: Reached maximum steps without finding a final answer."

    def _execute_tool(self, tool_name: str, args: str) -> str:
        """
        Execute tools dynamically by checking the 'func' key in the tools list.
        """
        for tool in self.tools:
            if tool['name'] == tool_name:
                # Kiểm tra xem tool có chứa hàm thực thi Python (callable) không
                if 'func' in tool and callable(tool['func']):
                    try:
                        # Gọi hàm với tham số (dưới dạng chuỗi string)
                        result = tool['func'](args)
                        return str(result)
                    except Exception as e:
                        return f"Error inside tool {tool_name}: {str(e)}"
                else:
                    return f"Configuration Error: Tool '{tool_name}' is missing a callable 'func'."
                    
        return f"Tool Error: '{tool_name}' not found in available tools."
