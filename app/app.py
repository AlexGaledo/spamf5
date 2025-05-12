from flask import Flask,jsonify
from flask_cors import CORS
from routes.chatbot_response import getChatbotResponse_bp
from routes.itenary_planner import itenary_bp
from routes.image_analyzer import analyzer_bp
from routes.maps_locator import maps_locator_bp
from routes.voice_recog import voice_bp



app = Flask(__name__)
app.register_blueprint(getChatbotResponse_bp, url_prefix="/chatbot") # normal chatbot
app.register_blueprint(itenary_bp, url_prefix="/iplanner") # itenary planner
app.register_blueprint(analyzer_bp, url_prefix="/analyze") # image sacn
app.register_blueprint(maps_locator_bp, url_prefix="/maps-locator") # maps locator
app.register_blueprint(voice_bp, url_prefix="/voice") # voice recognition

@app.route("/",methods=["GET","POST"])
def home():
    return jsonify({
        "response":"spamF5 backend"
    })

if __name__ == "__main__":
    app.run(debug=True)