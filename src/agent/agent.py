from src.agent.state import AgentState
from src.tools.registry import execute_tool
from src.tools.schemas import TOOL_SCHEMAS


class Agent:
    MAX_ITERATIONS = 5

    def __init__(self,
                 generator):
        
        self.generator = generator


    def run(self, 
            question: str,
            documents):

        state = AgentState(question,
                           documents)

        while state.step < self.MAX_ITERATIONS:
            state.step += 1
            print(f"\n[Agent step {state.step}]")

            decision = self.generator.generate(question = question,
                                               documents = documents,
                                               tool_schemas=TOOL_SCHEMAS,
                                               observations=state.observations)

            response_type = decision.get("type")

            if response_type == "final_answer":
                state.final_answer = decision.get("answer",
                                                  "")
                return state, decision.get("strategy")

            if response_type == "tool_call":

                tool_name = decision.get("tool_name")
                arguments = decision.get("arguments",
                                         {})

                print(f"[Tool] {tool_name}")
                print(f"[Arguments] {arguments}")

                try:

                    tool_result = execute_tool(tool_name,
                                               arguments)

                    print(f"[result] {tool_result}")

                    state.observations.append({"step": state.step,
                                               "tool": tool_name,
                                               "arguments": arguments,
                                               "result": tool_result})

                except Exception as e:

                    print(f"[Tool Error] {e}")

                    state.observations.append({"step": state.step,
                                               "tool": tool_name,
                                               "arguments": arguments,
                                               "error": str(e)})

                continue
                    
            # -------------------------
            # INVALID RESPONSE
            # -------------------------

            raise ValueError(f"Invalid response type: "
                             f"{response_type}")

        return ("The agent could not complete "
                "the task within the maximum "
                "number of steps.")


