from langchain_community.embeddings import BedrockEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.chat_models import BedrockChat


# LLM (Large Language Model) 생성 함수
def create_llm():
    model_kwargs = {
        "max_tokens": 2000,
        "temperature": 0
    }
    llm = BedrockChat(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs=model_kwargs
    )
    return llm


# PDF 파일 로드 함수
def load_pdf(file_path):
    loader = PyPDFLoader(file_path=file_path)
    return loader


# 텍스트 분할기 생성 함수
def create_text_splitter(chunk_size=1000, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter


# 임베딩 생성 함수
def create_embeddings(model_id="amazon.titan-embed-text-v2:0"):
    embeddings = BedrockEmbeddings(model_id=model_id)
    return embeddings


# 벡터 인덱스 생성 함수
def create_vector_index(embeddings, text_splitter, loader):
    index_creator = VectorstoreIndexCreator(
        vectorstore_cls=FAISS,
        embedding=embeddings,
        text_splitter=text_splitter
    )
    index_from_loader = index_creator.from_loaders([loader])
    return index_from_loader


# RAG (Retrieval-Augmented Generation) 응답 생성 함수
def generate_rag_response(index, question, llm):
    response_text = index.query(question=question, llm=llm)
    return response_text
