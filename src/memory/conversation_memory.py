from collections import deque


class ConversationMemory:

    def __init__(self, 
                 max_messages=10):

        self.messages = deque(maxlen=max_messages)

    def add(self, 
            role, 
            content):
        
        self.messages.append({"role": role,
                              "content": content})

    def get_messages(self):
        return list(self.messages)

    def clear(self):
        self.messages.clear()