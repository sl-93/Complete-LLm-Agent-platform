import re

class ChunkDocuments:
    def __init__(self,
                 documents):

        self.documents = documents

    def split_sentences(self,
                        text):

        return re.split(r'(?<=[.!?])\s+',
                        text)

    def chunk_text(self,
                   text,
                   max_chunks=500,
                   overlap_sentences=1):
        
        sentences = self.split_sentences(text)

        chunks = []
        current = []

        for sentence in sentences:
            candidate = " ".join(current + [sentence])

            if len(candidate) <= max_chunks:
                current.append(sentence)

            else:
                if current:
                    chunks.append(" ".join(current))

                current = (current[-overlap_sentences:] + [sentence])

        if current:
            chunks.append(" ".join(current))

        return chunks

    def chunk_documents(self):

        chunks = []

        for document in self.documents:

            text = document["text"]
            metadata = document["metadata"]

            text_chunks = self.chunk_text(text)

            for i, chunk in enumerate(text_chunks):

                chunk_metadata = metadata.copy()

                chunk_metadata["chunk_id"] = i

                chunks.append({"text": chunk,
                               "metadata": chunk_metadata})

        return chunks


    
    