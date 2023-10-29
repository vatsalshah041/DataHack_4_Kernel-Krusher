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
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_KEY")
# openai.api_key = OPENAI_API_KEY
OPENAI_API_KEY = ''

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

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if a file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def root():
    return jsonify({'home':True})

UPLOAD_FOLDER = 'static\\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False 

    for file in files:      
        if file and allowed_file(file.filename,ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

@app.route('/result', methods=['POST','GET'])
def result():
    try:
        # data = request.args.get('query')
        user_query = request.form['query']
        print(user_query)
        response = get_ans(user_query)

        return jsonify({"response": str(response)})
    except Exception as e:
        return jsonify({"error": str(e)})


model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")
# Load or create your Faiss index and make sure it's available in the 'index' variable.

def get_ans(query):
    embed = model.encode(query, convert_to_tensor=True)

    result_list = embed.numpy().astype(float).tolist()
    index = pinecone.Index('dh')
    response = index.query(
        vector=result_list,
        top_k=1,
        include_values=False,
        include_metadata=True,
    ).matches

    if response:
        resp = response[0].metadata
        resp = resp['text']
        restructured_resp = restructure(query,resp)
        return restructured_resp
    else:
        return "No matching result found"

    
    
def restructure(query, ans):
    print("restructuring")
    openai.api_key = OPENAI_API_KEY
    api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{
        "role": "system",
        "content": f"""The response to the query "{query}" was obtained by conducting a similarity search on a document, resulting in the answer: "{ans}". To best cater to the user's query, restructure this answer in a more suitable format.""",
    }],
    api_key=api_key,
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message.content

    
def test():
    print(pinecone.describe_index('dh'))


@app.route("/lang", methods=["GET", "POST"])
def language_select():
    if request.method == "POST":
        language = request.form["language"]
        response_data = {language}
        return jsonify(response_data)
    

if __name__ == '__main__':
    app.run(debug=True,host='localhost',port=5000)