from flask import Flask,jsonify
from flask_cors import CORS
from routes.chatbot_response import getChatbotResponse_bp

app = Flask(__name__)
app.register_blueprint(getChatbotResponse_bp, url_prefix="/chatbot")
CORS(app)

@app.route("/",methods=["GET","POST"])
def home():
    return jsonify({
        "response":"spamF5 backend"
    })

if __name__ == "__main__":
    app.run(debug=True)
