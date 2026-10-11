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
            documents,
            plan=None):

        state = AgentState(question,
                           documents)
        state.plan = plan or []

        while state.step < self.MAX_ITERATIONS:
            state.step += 1
            print(f"\n[Agent step {state.step}]")

            if state.plan:
                execution_question = (f"Original user goal: {state.question}\n"
                                      f"Current plan: {state.plan}\n"
                                      f"Execute plan step {state.current_step + 1}: "
                                      f"{state.plan[state.current_step]}")
            else:
                execution_question = state.question

            decision = self.generator.generate(question=execution_question,
                                               documents=state.documents,
                                               tool_schemas=TOOL_SCHEMAS,
                                               observations=state.observations)

            response_type = decision.get("type")

            if response_type == "final_answer":
                state.final_answer = decision.get("answer",
                                                  "")
                if not state.plan:
                    return state.final_answer, decision.get("strategy")
                
                # Record the completed plan step.
                state.observations.append({"step": state.current_step + 1,
                                           "type": "plan_step_completed",
                                           "description": state.plan[state.current_step],
                                           "result": state.final_answer})
                state.current_step += 1

                # All planned steps are complete.
                if state.current_step >= len(state.plan):
                    return state.final_answer, decision.get("strategy")

                # Ask the LLM to execute the next step.
                continue

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


