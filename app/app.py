from flask import Flask,jsonify
from flask_cors import CORS
from .routes.chatbot_response import getChatbotResponse_bp
from .routes.itenary_planner import itenary_bp
from .routes.image_analyzer import analyzer_bp


app = Flask(__name__)
app.register_blueprint(getChatbotResponse_bp, url_prefix="/chatbot") # normal chatbot
app.register_blueprint(itenary_bp, url_prefix="/iplanner") # itenary planner
app.register_blueprint(analyzer_bp, url_prefix="/analyze") # image sacn
CORS(app)

@app.route("/",methods=["GET","POST"])
def home():
    return jsonify({
        "response":"spamF5 backend"
    })

if __name__ == "__main__":
    app.run(debug=True)
