from flask import Blueprint, jsonify, request
from services.gemini import getChatbotResponse

#personal chatbot
getChatbotResponse_bp = Blueprint("chatbot", __name__)


@getChatbotResponse_bp.route("/",methods=["POST"])
def geminiResponse():
    #instructions para sa casual-bot
    sysin = """
        You are a helpful AI travel assistant AI, first you will introduce yourself as baybay.ai,
        you can also recognize local Filipino Dialects.
        """
    
    sysin = ""
    data = request.get_json()
    user_input = data.get("input","")
    if not user_input:
        return jsonify({
            "response":"no input/message provided."
        }),400
    
    response = getChatbotResponse(user_input,sysin)["response"]

    return jsonify({
        "response":response
    })



