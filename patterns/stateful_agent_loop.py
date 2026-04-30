"""
Stateful agent loop with tool dispatch

Real scenario: this is the core of any agentic system — LangChain, AutoGPT, Claude's tool use, all of them. 
An agent receives a goal, reasons about what to do, calls a tool, observes the result, updates its memory, 
and loops until it decides it's done. You're implementing the orchestration layer — not the LLM, 
not the tools, but the loop that connects them.
"""
from dataclasses import dataclass, field

@dataclass
class AgentState:
    goal: str
    memory: list = field(default_factory=list)
    tool_results: list = field(default_factory=list)
    status: str = "running"  # running | done | failed

class Agent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.max_steps = 10

    def run(self, goal, system_prompt=""):
        state = AgentState(
            goal=goal,
            memory=[system_prompt, goal],
        )

        for step in range(self.max_steps):
            action = self.llm(state.memory)

            if action.type == "tool_call":
                if action.tool_name not in self.tools:
                    state.memory.append(f"Error: tool '{action.tool_name}' not found")
                    continue

                try:
                    result = self.tools[action.tool_name](action.tool_input)
                    state.tool_results.append(result)
                    state.memory.append(f"Tool '{action.tool_name}' returned: {result}")
                except Exception as e:
                    error_msg = f"Tool '{action.tool_name}' failed: {e}"
                    state.memory.append(error_msg)  # LLM sees the failure and reasons about it

            elif action.type == "final_answer":
                state.status = "done"
                return action.response

        state.status = "failed"
        return "max steps reached"