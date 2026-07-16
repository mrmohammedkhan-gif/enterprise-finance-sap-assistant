from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"


def load_policy_documents() -> list[Document]:
    """Load all finance policy text files."""
    documents: list[Document] = []

    for file_path in sorted(DATA_FOLDER.glob("*.txt")):
        content = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not content:
            continue

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": file_path.name,
                    "path": str(file_path),
                },
            )
        )

    if not documents:
        raise RuntimeError(
            f"No policy documents found in {DATA_FOLDER}"
        )

    return documents


def build_policy_retriever():
    """Create an in-memory semantic policy retriever."""
    documents = load_policy_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
    )

    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
    )

    vector_store = InMemoryVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )


policy_retriever = build_policy_retriever()


def search_finance_policies(
    query: str,
) -> list[Document]:
    """Return policy passages relevant to a question."""
    return policy_retriever.invoke(query)


if __name__ == "__main__":
    question = (
        "What is the company policy for approving "
        "invoices above £10,000?"
    )

    results = search_finance_policies(question)

    print(f"\nQuestion: {question}\n")

    for number, document in enumerate(results, start=1):
        print(f"Result {number}")
        print(
            f"Source: "
            f"{document.metadata.get('source', 'unknown')}"
        )
        print(document.page_content)
        print("-" * 60)