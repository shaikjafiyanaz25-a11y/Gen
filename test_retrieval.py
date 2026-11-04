from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

question = "What are the cardiology OPD timings?"

results = vectorstore.similarity_search(question, k=3)

print("\n===== RAG SEARCH RESULTS =====\n")

for i, result in enumerate(results, 1):
    print(f"--- Result {i} ---")
    print(result.page_content)
    print()