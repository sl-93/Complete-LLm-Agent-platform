from pathlib import Path
from src.vectorstore.index_documents import indexing
from src.pipeline.agent_pipeline import AgentPipeline


DATA_PATH = "data"
DB_PATH = "chroma_db"

EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "gemma4:e2b"

COLLECTION_NAME = "documents"


def build_database():

    db_exists = Path(DB_PATH).exists()

    if not db_exists:

        print("Building vector database...")

        indexing(DATA_PATH,
                 EMBEDDING_MODEL,
                 DB_PATH,
                 COLLECTION_NAME)

        print("Vector database created.")


def main():

    build_database()

    pipeline = AgentPipeline(EMBEDDING_MODEL,
                             DB_PATH,
                             COLLECTION_NAME,
                             LLM_MODEL,
                             query_mode = "original",   # original | rewrite | multi_query
                             retrieval_mode = "hybrid", # dense | bm25 | hybrid
                             top_k = 5,
                             num_queries = 3)

    while True:

        question = input("\nYou: ").strip()

        if question.lower() in {"exit",
                                "quit"}:
            break

        result, strategy = pipeline.answer(question)

        print("\nStrategy:",strategy)

        print("\nAnswer:")

        print(result.final_answer)


if __name__ == "__main__":
    main()