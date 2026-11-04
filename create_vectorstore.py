import os

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv


load_dotenv()

DOCUMENTS_FOLDER = "documents"
VECTORSTORE_FOLDER = "vectorstore"


def load_documents():
    documents = []

    for filename in os.listdir(DOCUMENTS_FOLDER):

        file_path = os.path.join(DOCUMENTS_FOLDER, filename)

        if filename.endswith(".txt"):
            loader = TextLoader(
                file_path,
                encoding="utf-8"
            )
            documents.extend(loader.load())

        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())

    return documents


def main():

    print("Loading hospital documents...")

    documents = load_documents()

    if not documents:
        print("No documents found!")
        return

    print(f"Loaded {len(documents)} document pages/files.")

    # Split documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    # Create Gemini embeddings
    print("Creating Gemini embeddings...")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    # Create FAISS vector database
    print("Creating FAISS vector database...")

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    # Save vector database
    vectorstore.save_local(VECTORSTORE_FOLDER)

    print()
    print("====================================")
    print("RAG VECTOR DATABASE CREATED!")
    print("====================================")
    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")
    print(f"Saved to: {VECTORSTORE_FOLDER}")


if __name__ == "__main__":
    main()