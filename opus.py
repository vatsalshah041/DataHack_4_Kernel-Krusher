from transformers import AutoTokenizer, MarianMTModel
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter
import os,asyncio,time
from PyPDF2 import PdfReader
from typing_extensions import Concatenate

# pdf generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


sample_fr_text = """36.  Le 9 juillet 2014, soit environ quatre ans et quatre mois plus tard, le 
tuteur H.K. saisit le tribunal d’instance de Nazilli pour demander la levée de 
la mesure de tutelle. Rappelant que l’hôpital avait auparavant précisé qu’un 
rétablissement de son épouse était possible sous traitement approprié 
(paragraphe 21 ci-dessus), il soutint que la requérante ne montrait désormais 
plus  aucun  symptôme  franc  de  maladie.  Partant,  H.K.  demanda  que  deux 
hôpitaux  universitaires  soient  chargés  de  procéder  à  une  nouvelle  expertise 
psychiatrique."""


def create_pdf(text_array):
    pdf_file = "D:\\DATAHACK\\Datahack2024\\translated_pdfs\\translation2"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()
    for text in text_array:
        elements.append(Paragraph(text, styles["Normal"]))

    doc.build(elements)
    print(f"PDF generated: {pdf_file}")

class TranslationService:
    def __init__(self, src, trg):
        self.src = src
        self.trg = trg
        self.model_name = f"Helsinki-NLP/opus-mt-{src}-{trg}"
        self.model = MarianMTModel.from_pretrained(self.model_name, cache_dir='./opus_config')
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    async def Fr2En(self, text):
        batch = self.tokenizer([text], return_tensors="pt")
        generated_ids = self.model.generate(**batch)
        output = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return output

    async def translate_texts(self, texts):
        tasks = [self.Fr2En(text) for text in texts]
        tts = await asyncio.gather(*tasks)
        return tts
    

def get_documents(pdf_path):
    pdfreader = PdfReader(pdf_path)
    
    raw_text = ''
    for i,page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            raw_text += content

    text_splitter = CharacterTextSplitter(
    separator='\n',
    chunk_size= 800,
    chunk_overlap = 200,
    length_function = len
    )

    texts = text_splitter.split_text(raw_text)

    return texts


def translate_docs(path='D:\\DATAHACK\\Datahack2024\\SearchEnginePDFs\\pdfs\\AFFAIRE C.P. ET M.N. c. FRANCE.pdf'):
    chunk_of_texts = get_documents(path)

    translation_service = TranslationService(src="fr", trg="en")
    translation_tasks = [translation_service.translate_texts([text]) for text in chunk_of_texts]

    # Run the tasks asynchronously
    loop = asyncio.get_event_loop()
    translated_texts = loop.run_until_complete(asyncio.gather(*translation_tasks))
    translated_texts = [texts[0]+"\n" for texts in translated_texts]

    create_pdf(translated_texts)

translate_docs()



