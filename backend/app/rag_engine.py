from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import create_retriever_tool
from app.config import DATA_DIR, GEMINI_API_KEY

INDEX_DIR = DATA_DIR.parent / ".faiss_index"

def get_auto_retriever_tool():
    # Load documents from the data directory
    loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()

    # Split documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    split_documents = text_splitter.split_documents(documents)

    # Reuse the local index so embeddings are not regenerated on every restart.
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GEMINI_API_KEY
    )

    if (INDEX_DIR / "index.faiss").exists():
        vectorstore = FAISS.load_local(
            str(INDEX_DIR),
            embeddings,
            allow_dangerous_deserialization=True,
        )
    else:
        vectorstore = FAISS.from_documents(split_documents, embeddings)
        vectorstore.save_local(str(INDEX_DIR))

    # Create a retriever tool from the vector store
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return create_retriever_tool(
        retriever, 
        name="AutoRetriever", 
        description="Un outil pour récupérer des documents pertinents concernant l'histoire de l'automobile dans le répertoire de données."
        )