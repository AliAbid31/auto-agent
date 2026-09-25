from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecusiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.tools.retriever import create_retriever_tool
from app.config import DATA_DIR, GEMINI_API_KEY

def get_auto_retriever_tool():
    # Load documents from the data directory
    loader = DirectoryLoader(DATA_DIR, glob="**/*.md", loader_cls=TextLoader, encoding="utf-8")
    documents = loader.load()

    # Split documents into smaller chunks
    text_splitter = RecusiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    split_documents = text_splitter.split_documents(documents)

    # Create embeddings for the split documents
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=GEMINI_API_KEY
    )
    
    # Create a FAISS vector store from the embeddings
    vectorstore = FAISS.from_documents(split_documents, embeddings)

    # Create a retriever tool from the vector store
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return create_retriever_tool(
        retriever, 
        name="AutoRetriever", 
        description="Un outil pour récupérer des documents pertinents concernant l'histoire de l'automobile dans le répertoire de données."
        )