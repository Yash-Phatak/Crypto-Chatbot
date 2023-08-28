from flask import jsonify,Flask,render_template,request,send_file
from flask_cors import CORS
from chat import chatbot_response
from api import get_realtime
from analysis import highplot
from analysis import cryptocurrencies
from analysis import compareit
import difflib
import random
import io

app = Flask(__name__)
api_v2_cors_config = {
  "origins": ["*"],
  "methods": ["OPTIONS", "GET", "POST"],
  "allow_headers": ["Authorization", "Content-Type"]
}
CORS(app, resources={r'/*': api_v2_cors_config})

@app.get("/")
def index_get():    
    return "Hello"

# @app.post("/faq")
# def faq():
#     text = request.get_json().get("message")
#     # print(type(text))
#     answer = chatbot_response(text)
#     # message = {"answer":response}
#     return jsonify(answer)

@app.post("/faq")
def faq():
    text = request.get_json().get("message")
    answer = chatbot_response(text)
    answer.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify(answer)


@app.post("/plot")
def plot():
    buffer = io.BytesIO()
    text = request.get_json().get("message")
    if text.lower() in cryptocurrencies:
        plot = highplot(text)
        plot.savefig(buffer, format='png')
        buffer.seek(0)
    else:
        selected_name = difflib.get_close_matches(text,cryptocurrencies)
        if selected_name:
            final_name = random.choice(selected_name)
            plot = highplot(final_name)
            plot.savefig(buffer, format='png')
            buffer.seek(0)
    plot.close()
    return send_file(buffer, mimetype='image/png')

@app.post("/comparison")
def comparison():
    buffer = io.BytesIO()
    text = request.get_json().get("message")
    text1 = text.split()[0]
    text2 = text.split()[1]
    plot = compareit(text1, text2)
    plot.savefig(buffer, format='png')
    buffer.seek(0)
    plot.close()
    return send_file(buffer, mimetype='image/png')

@app.post("/realtime")
def realtime():
    text = request.get_json().get("message")
    answer = get_realtime(text)
    return jsonify(answer)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'https://crypton-chatbot.vercel.app')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

if __name__ == "__main__":
    app.run(debug=True)