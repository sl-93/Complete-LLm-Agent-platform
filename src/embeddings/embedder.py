import ollama


class Embedder:

    def __init__(self,
                 embedding_model):

        self.model = embedding_model 

    def encode(self, texts):

        return [ollama.embeddings(model=self.model,
                                  prompt=text)["embedding"]
                                  for text in texts
                                  if text.strip()]