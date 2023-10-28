import os
import openai
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from sentence_transformers import SentenceTransformer

pinecone.init(      
	api_key='b0b2574e-0973-49a8-a210-196772f9d1b2',      
	environment='gcp-starter'      
)      
index = pinecone.Index('datahack')


def create_index(path, index):
    loader_cls = PyPDFLoader
    loader = loader_cls(path)
    documents = loader.load()
   
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    embeddings = SentenceTransformerEmbeddings(model_name="multi-qa-mpnet-base-dot-v1")
    db = Pinecone.from_documents(texts, embeddings, index_name = index)
    print('done')
    
model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")

def get_ans(query):
    embeddings = model.encode(query, convert_to_tensor=True)
    print(type(embeddings.numpy()))

    fin = embeddings.numpy()[0]
    # elements = fin.strip('[]').split()

# Convert the elements to float and create a list
    result_list = [float(element) for element in embeddings.numpy()[0]]
    print(len(result_list))
    resp = index.query(
        vector=result_list,
        top_k=3,
        include_values=False,
        include_metadata=True,
    )
    print(resp)
    #resp.matches[0,1,2] as per score
    

    
    
if __name__ == '__main__':
    path = "C:\\Users\\Hp\\Desktop\\data\\CASE OF KURT v. AUSTRIA.pdf"
    # create_index(path, 'datahack')
    get_ans(['The European Court of Human Rights, sitting as a Grand Chamber composed of:'])