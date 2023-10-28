from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import torch

import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/mbart-large-50-many-to-many-mmt"
headers = {"Authorization": "Bearer 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","src_lang":'hi_IN',"tgt_lang":''}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "Меня зовут Вольфганг и я живу в Берлине"
})

print(output)