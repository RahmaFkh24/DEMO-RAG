##Imports and vectorEnvironment Setup

import gradio as gr
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Load environment variables from the .env file
load_dotenv()
#Loading the PDF Document
print("Loading PDF document...")
loader = PyPDFLoader("TechCorp_Official_Employee_Handbook.pdf")
document = loader.load()

print(document[0].page_content)

# chunking the document into smaller pieces
print("Chunking text...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50 # to relate the chunks to each other and provide meaning between the chunks
)
chunks = text_splitter.split_documents(document)

print(chunks[0].page_content)
#Creating Embeddings and Initializing the Vector DB
print("Creating  database...")
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
vector_db = Chroma.from_documents(
    documents=chunks, 
    embedding=embeddings, 
    persist_directory="./chroma_db"
)

##Setting Up the Retriever and Prompt Template
# Configure the database to act as a document retriever
retriever = vector_db.as_retriever(search_kwargs={"k": 2})

# Define the hidden prompt structure for the LLM
template = """
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Use three sentences maximum and keep the answer concise.

Context: {context}

Question: {question}

Answer:
"""
prompt = PromptTemplate.from_template(template)
# Initializing the LLM and Constructing the RAG Chain
# Initialize the free Gemini model tier
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)

# Helper function to stitch retrieved chunks into a single text block
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Connect everything together using LangChain Expression Language (LCEL)
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
)

def answer_question(message: str, _history: list[dict[str, str]]) -> str:
    question = message
    if _history:
        conversation = "\n".join(
            f"{turn['role']}: {turn['content']}" for turn in _history[-4:]
        )
        question = f"Conversation history:\n{conversation}\n\nCurrent question: {message}"

    response = rag_chain.invoke(question)
    return response.text


demo = gr.ChatInterface(
    fn=answer_question,
    title="Employee Handbook Assistant",
    description="Ask a question about the employee handbook.",
    examples=[
        "What days can I work from home?",
        "What are the employment policies?",
    ],
)

if __name__ == "__main__":
    demo.launch()