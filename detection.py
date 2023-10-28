import pickle
import numpy as np
from flask import Flask, request, jsonify

with open('./model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('./vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        input_text = data.get('input_text')  # Use 'get' to handle missing key gracefully
        if input_text is None:
            return jsonify({'error': 'The input_text field is missing or empty.'})

        prediction = make_prediction(input_text)
        response = {'prediction': prediction}
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

def make_prediction(input_text):
    inputArray = np.array([input_text])
    vectorizedInput = vectorizer.transform(inputArray)
    prediction = model.predict(vectorizedInput)
    return prediction[0]  # Assuming the model returns a single prediction

if __name__ == '__main__':
    app.run(debug=True)
