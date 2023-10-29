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
import multiprocessing

openai.api_key = ''
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
   
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
    texts = text_splitter.split_documents(documents)
    print('embedding')
    embeddings = SentenceTransformerEmbeddings(model_name="multi-qa-mpnet-base-dot-v1")
    print('storing')
    db = Pinecone.from_documents(texts, embeddings, index_name = 'dh')
    print('done')
    
def create_index_2(path):
  loader_cls = PyPDFLoader
  loader = loader_cls(path)
  documents = loader.load()
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
  texts = text_splitter.split_documents(documents)
  embeddings = SentenceTransformerEmbeddings(model_name="multi-qa-mpnet-base-dot-v1")
  print('storing')
  db = Pinecone.from_documents(texts, embeddings, index_name = 'dh')
  print('done')


def get_ans(query):
    model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")
    embed = model.encode([query], convert_to_tensor=True)   #not for OAI
    
    # print(type(embed.numpy()))

    result_list = [float(element) for element in embed.numpy()[0]]

    resp = index.query(
        vector=result_list,
        top_k=1,
        include_values=False,
        include_metadata=True,
    ).matches[0].metadata
    return(resp['text'])
    #resp.matches[0,1,2] as per score
    
def restructure(query, ans):
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{
      "role": "system",
      "content": f'The answer to the question {query} recieved by performing similarity search on a document gave the answer {ans}. Based on the question, restructure the ans in a suitable answer for the user'
    }],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
  )

  return response.choices[0].message.content

def process_pdfs(pdf_path):
    create_index_2(pdf_path)
    
def call_multi(array):
  pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

  pool.map(process_pdfs, array)
  pool.close()
  pool.join()
    
def name_all_pdfs(path):
  array = []
  for filename in os.listdir(path):
    f = os.path.join(path, filename)
    array.append(f)
  call_multi(array)

if __name__ == '__main__':
    path = "C:\\Users\\Hp\\Desktop\\Code\\Datahack\\case"
    name_all_pdfs(path)
    # query = 'What was the outcome for the alleged violation of Article 8 in the case of ANAGNOSTAKIS v. GREECE?'
    # print('done')
    # make_ans = get_ans(query)
    # print(restructure(query,make_ans))