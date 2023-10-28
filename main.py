import os
import openai
from flask import Flask, render_template, Response, request,jsonify,redirect
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

app = Flask(__name__)

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
# def create_index(path):
#     print('deleting')
#     pinecone.delete_index('dh')
#     print('creating')
#     pinecone.create_index('dh', dimension=768, metric='cosine')
#     print('loading')
#     loader = DirectoryLoader(path, glob="./*.pdf", loader_cls=PyPDFLoader)
#     documents = loader.load()
#     # loader_cls = PyPDFLoader
#     # loader = loader_cls(path)
#     # documents = loader.load()
#     print('spliting')
   
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
#     texts = text_splitter.split_documents(documents)
#     print('embedding')
#     embeddings = SentenceTransformerEmbeddings(model_name="multi-qa-mpnet-base-dot-v1")
#     print('storing')
#     db = Pinecone.from_documents(texts, embeddings, index_name = 'dh')
#     print('done')

# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'pdf'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if a file has a valid extension
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return redirect(request.url)

#     file = request.files['file']

#     if file.filename == '':
#         return redirect(request.url)

#     if file and allowed_file(file.filename): 
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filepath)
#         return 'File uploaded successfully.'

#     return 'Invalid file format. Please upload a PDF file.'


# @app.route("/result", methods=["GET", "POST"])

# def get_ans():
#     if request.method=='POST':

#         query = request.get_json()

#         if not query:
#             return jsonify({"error": "No query provided"})

#         model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")
#         try:
#             embed = model.encode(query, convert_to_tensor=True)   #not for OAI
            
#             # print(type(embed.numpy()))

#             result_list = [float(element) for element in embed.numpy()[0]]
#             resp = index.query(
#                 vector=result_list,
#                 top_k=1,
#                 include_values=False,
#                 include_metadata=True,
#             ).matches[0].metadata   
#             return jsonify(resp['text']),200

#         except Exception as e:
#             print(e)
#             return jsonify({"error": str(e)}),400

model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")
# Load or create your Faiss index and make sure it's available in the 'index' variable.

def get_ans(query):
    embed = model.encode(query, convert_to_tensor=True)

    result_list = [float(element) for element in embed.numpy()[0]]
    # result_list = embed.numpy().tolist()[0]
    index = pinecone.Index('dh')
    resp = index.query(
        vector=result_list,
        top_k=1,
        include_values=False,
        include_metadata=True,
    ).matches[0].metadata
    return resp['text']

@app.route('/result', methods=['POST'])
def query():
    try:
        data = request.get_json()
        query = data['query']
        response = get_ans(query)

        response = get_ans(query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)})

    
def restructure(query, ans):
  api_key = "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"
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{
      "role": "system",
      "content": f'The answer to the question {query} recieved by performing similarity search on a document gave the answer {ans}. Based on the question, restructure the ans in a suitable answer for the user'
    }],
  api_key=api_key,
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
  )
  return response.choices[0].message.content

@app.route("/restructure", methods=["POST"])
def restructure_route():
    response = request.get('/result')
    if response.status_code == 200:
        query = request.get_json().get("query")  # Get the query from the request JSON
        resp = request.get_json().get("resp")  # Get the response from the request JSON

    if not query or not resp:
        return jsonify({"error": "Both query and resp are required for restructuring"})

    # Call the restructure function and get the restructured answer
    restructured_answer = restructure(query, resp)

    return jsonify({"restructured_answer": restructured_answer})


    
def test():
    print(pinecone.describe_index('dh'))


@app.route("/lang", methods=["GET", "POST"])
def language_select():
    if request.method == "POST":
        language = request.form["language"]
        response_data = {language}
        return jsonify(response_data)
    

if __name__ == '__main__':
    # path = "C:\\Users\\Dev Atul Patel\\Downloads\\datalaw\\Untitled folder\\AFFAIRE AVCIOgLU c. TÜRKiYE.pdf"
    # create_index(path)
    # print('done')
    # get_ans(['What was the outcome for the alleged violation of Article 8 in the case of ANAGNOSTAKIS v. GREECE?'])
    app.run(debug=True)