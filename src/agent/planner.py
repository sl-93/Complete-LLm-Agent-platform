import json


class Planner:

    def __init__(self, 
                 generator):
        
        self.generator = generator

    def create_plan(self, question):

        raw_response = self.generator.generate_plan(question=question)

        try:
            result = json.loads(raw_response)
            plan = result["plan"]

        except (json.JSONDecodeError, KeyError, TypeError):
            raise ValueError("Planner returned invalid JSON.")

        if (not isinstance(plan, list)
            or not plan
            or not all(isinstance(item, str) and item.strip()
                       for item in plan)):
            
            raise ValueError("Planner must return a non-empty list "
                             "of non-empty step descriptions.")

        return plan