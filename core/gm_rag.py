import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from sentence_transformers import CrossEncoder

from dotenv import load_dotenv


load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"token": os.getenv("HF_TOKEN")},
)

cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

BASE_DIR = os.path.dirname( os.path.dirname(os.path.abspath(__file__)) )
PATH_EMBEDDINGS = os.path.join(BASE_DIR, "resources", "embeddings")
PATH_PDF = os.path.join(BASE_DIR, "resources", "GameLore_Resource.pdf")


def get_vectorstore():

    if os.path.exists(PATH_EMBEDDINGS) and os.listdir(PATH_EMBEDDINGS):  # Check if the directory exists and is not empty
        vectordb = Chroma(persist_directory=PATH_EMBEDDINGS, embedding_function=embeddings)
        return vectordb
    
    doc_loader = PyMuPDFLoader(PATH_PDF)
    loaded_doc  =  doc_loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(loaded_doc)

    vectordb = Chroma.from_documents(chunks, embeddings, persist_directory=PATH_EMBEDDINGS)

    return vectordb

def retrieve_information(query, vectordb, top_k=5):
    
    docs = vectordb.similarity_search(query, k= (top_k*4)) # Retrieve more documents than needed for re-ranking
    
    pairs = [[query, doc.page_content] for doc in docs]
    scores = cross_encoder.predict(pairs)
    scored_docs = list(zip(scores, docs ))
    scored_docs.sort(key=lambda x: x[0], reverse=True)  # Sort by score in descending order
    top_docs = [doc for score, doc in scored_docs[:top_k]]  # Get top-k documents based on scores
    return top_docs