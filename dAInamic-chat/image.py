from flask import Flask, jsonify, request, render_template
import requests
from translate import Translator
app = Flask(__name__)


API_URL ="https://stable-diffusion-v2.p.rapidapi.com/stable-diffusion"
headers = {
        "X-RapidAPI-Key": "c5940c5c50mshe6781557d4ecd87p133462jsn54187cf08e97",
        "X-RapidAPI-Host": "stable-diffusion-v2.p.rapidapi.com"
    }

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

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
        response = requests.get(API_URL, headers=headers, params=querystring)
        
        return render_template("imgbot.html", input_text=input_text, output=response.json())
    else:
        return render_template("imgbot.html")
    

if __name__ == '__main__':
    app.run(debug=True)



    # def image(input_text):


    # url = "https://stable-diffusion-v2.p.rapidapi.com/stable-diffusion"

    # querystring = {"description":input_text}

    
    

    # return(response.json())