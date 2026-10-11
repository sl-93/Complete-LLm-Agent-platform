class AgentState:

    def __init__(self, 
                 question, 
                 documents):
        
        self.question = question
        self.documents = documents
        self.plan = []
        self.current_step = 0
        self.observations = []
        self.step = 0
        self.final_answer = None