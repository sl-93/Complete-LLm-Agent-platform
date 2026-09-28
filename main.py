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

    pipeline = AgentPipeline(embedding_model=EMBEDDING_MODEL,
                             llm_model=LLM_MODEL,
                             db_path=DB_PATH,
                             collection_name=COLLECTION_NAME,
                             top_k=5)

    while True:

        question = input("\nYou: ").strip()

        if question.lower() in {"exit",
                                "quit"}:
            break

        result = pipeline.answer(question)

        print("\nStrategy:",
              result["strategy"])

        print("\nAnswer:")

        print(result["answer"])


if __name__ == "__main__":
    main()