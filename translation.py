from flask import Flask, request, jsonify
from easygoogletranslate import EasyGoogleTranslate

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        data = request.get_json(force=True)
        text_to_translate = data.get('text_to_translate')
        print(text_to_translate)

        try:
            translator = EasyGoogleTranslate()
            
            # Translate to Spanish
            spanish_translation = translator.translate(text_to_translate, target_language='es')
            
            # Translate to French
            french_translation = translator.translate(text_to_translate, target_language='fr')

            result = {
                'original_text': text_to_translate,
                'spanish_translation': spanish_translation,
                'french_translation': french_translation
            }

            return jsonify(result)
        except Exception as e:
            error_message = f"Translation error: {str(e)}"
            return jsonify({'error': error_message}), 500  # Return an error response with status code 500

if __name__ == '__main__':
    app.run(debug=True)
