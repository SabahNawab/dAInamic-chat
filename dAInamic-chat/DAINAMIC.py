from flask import Flask, jsonify, request, render_template

import requests
from translate import Translator

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-1-pythia-12b"
headers = {"Authorization": "Bearer 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"}

API_URL2 ="https://stable-diffusion-v2.p.rapidapi.com/stable-diffusion"
headers2 = {
        "X-RapidAPI-Key": "c5940c5c50mshe6781557d4ecd87p133462jsn54187cf08e97",
        "X-RapidAPI-Host": "stable-diffusion-v2.p.rapidapi.com"
    }

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload,timeout=60)
    print(response.content)
    return response.json()

def query2(payload):
    response = requests.post(API_URL2, headers=headers2, json=payload)
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        input_l = request.form['input_language']
        input_text = request.form['input_text']
        
        if "german" in input_l.lower():
            selected_lang = 'de'
        elif "french" in input_l.lower():
            selected_lang = 'fr'
        elif "chinese" in input_l.lower():
            selected_lang = 'zh'
        else:
            selected_lang = 'en' 
        
        translator = Translator(from_lang=selected_lang , to_lang="en")
        translation = translator.translate(input_text)

        if ("hi" ) in translation.lower():
            translator= Translator(from_lang='en', to_lang=selected_lang )
            
            output="Hi, How may I help you today "
            translation = translator.translate(output)
        elif ("hello" ) in translation.lower():
            output="Hello, How may I help you today "
            translator= Translator(from_lang='en', to_lang=selected_lang )
            translation = translator.translate(output)
        
        else:
            if "?" not in translation:
                translation=translation+" ?"
            output = query({
                "inputs": translation,
                "options": {"wait_for_model": True,"max_length": 1024}
            })
            
            l = len(translation)
            out__=(str(output)[25+l:-3])
            translator= Translator(from_lang='en', to_lang=selected_lang )
            translation = translator.translate(out__)
            # translation=out__
           
        return render_template("textbot.html", input_text=input_text,  output=translation)
    else:
        return render_template("textbot.html")
    
@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        input_l = request.form['input_language']
        input_text = request.form['input_text']
        
        if "german" in input_l.lower():
            selected_lang = 'de'
        elif "french" in input_l.lower():
            selected_lang = 'fr'
        elif "chinese" in input_l.lower():
            selected_lang = 'zh'
        else:
            selected_lang = 'en' 
        
        translator = Translator(from_lang=selected_lang , to_lang="en")
        translation = translator.translate(input_text)
        querystring = {"description":translation}
        response = requests.get(API_URL2, headers=headers2, params=querystring)
        
        return render_template("imgbot.html", input_text=input_text, output=response.json())
    else:
        return render_template("imgbot.html")
if __name__ == '__main__':
    app.run(debug=True)
