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
index = pinecone.Index('dh')

global embeddings
global model
# embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', show_progress_bar=True, openai_api_key='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')
# embeddings = SentenceTransformerEmbeddings("sentence-transformers/multi-qa-mpnet-base-dot-v1")

#pinecone.create_index("example-index", dimension=128, metric="euclidean", pods=4, pod_type="s1.x1")
#pinecone.delete_index('dh')
def create_index(path):
    print('deleting')
    pinecone.delete_index('dh')
    print('creating')
    pinecone.create_index('dh', dimension=768, metric='cosine')
    print('loading')
    loader = DirectoryLoader(path, glob="./*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    # loader_cls = PyPDFLoader
    # loader = loader_cls(path)
    # documents = loader.load()
    print('spliting')
   
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    print('embedding')
    embeddings = SentenceTransformerEmbeddings(model_name="multi-qa-mpnet-base-dot-v1")
    print('storing')
    db = Pinecone.from_documents(texts, embeddings, index_name = 'dh')
    print('done')


def get_ans(query):
    model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")
    embed = model.encode(query, convert_to_tensor=True)   #not for OAI
    
    # print(type(embed.numpy()))

    result_list = [float(element) for element in embed.numpy()[0]]
    print((result_list))
    resp = index.query(
        vector=result_list,
        top_k=3,
        include_values=False,
        include_metadata=True,
    )
    print(resp)
    #resp.matches[0,1,2] as per score
    
def test():
    print(pinecone.describe_index('dh'))

if __name__ == '__main__':
    path = "C:\\Users\\Hp\\Desktop\\Code\\Datahack\\case"
    create_index(path)
    print('done')
    get_ans(['What was the outcome for the alleged violation of Article 8 in the case of ANAGNOSTAKIS v. GREECE?'])