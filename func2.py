import os
import openai, torch
import pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from transformers import pipeline
from langchain.chains import RetrievalQA
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM 
from langchain.llms import HuggingFacePipeline

pinecone.init(      
	api_key='b0b2574e-0973-49a8-a210-196772f9d1b2',      
	environment='gcp-starter'      
)      
index = pinecone.Index('dh')

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
    db = Pinecone.from_documents([t.page_content for t in texts], embeddings, index_name = 'dh')
    print('done')


# def get_ans(query):
#     model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")
#     embed = model.encode(query, convert_to_tensor=True)   #not for OAI
    
#     # print(type(embed.numpy()))

#     result_list = [float(element) for element in embed.numpy()[0]]
#     print((result_list))
#     resp = index.query(
#         vector=result_list,
#         top_k=3,
#         include_values=False,
#         include_metadata=True,
#     )
#     print(resp)
#     #resp.matches[0,1,2] as per score

checkpoint = "MBZUAI/LaMini-Flan-T5-783M"     #google/flan-t5-xl  google/flan-t5  MBZUAI/LaMini-Flan-T5-783M
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelForSeq2SeqLM.from_pretrained(
    checkpoint,
    device_map="auto",
    torch_dtype = torch.float32)

embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")

# db = Chroma(persist_directory="data", embedding_function=embeddings)

pipe = pipeline(
    'text2text-generation',
    model = base_model,
    tokenizer = tokenizer,
    max_length = 512,
    do_sample = True,
    temperature = 0.3,
    top_p= 0.95
)
local_llm = HuggingFacePipeline(pipeline=pipe)

qa_chain = RetrievalQA.from_chain_type(llm=local_llm,
        chain_type='stuff',
        retriever=db.as_retriever(search_type="similarity", search_kwargs={"k":2}),
        return_source_documents=True,
        )
    
def test():
    print(pinecone.describe_index('dh'))

if __name__ == '__main__':
    # path = "C:\\Users\\Hp\\Desktop\\Code\\Datahack\\case"
    # create_index(path)
    print('done')
    # get_ans(['What was the outcome for the alleged violation of Article 8 in the case of ANAGNOSTAKIS v. GREECE?'])