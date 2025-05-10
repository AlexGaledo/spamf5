from flask import Blueprint,request,jsonify
from services.gemini import getChatbotResponse

#itenary planner
itenary_bp = Blueprint("/itenary",__name__)


@itenary_bp.route("/",methods=["POST"])
def generatePlanner():
    try:
        #instruction para sa planner bot
        sysin = """
            You are a helpful AI travel assistant that creates detailed, culturally-informed itineraries/travel planner tailored to the selected destination. 
            Your recommendations should reflect local customs, traditions, food, and unique experiences relevant to the culture chosen.
            """
        
        data = request.get_json()
        user_input = data.get("input","")
        location = data.get("location", "not specified")
        response = getChatbotResponse(user_input,sysin,location)
        chatbot_resp = response["response"]
        location = response["location"]
        return jsonify({
            "location chosen":location,
            "response": chatbot_resp
        })
    except Exception as e:
        return jsonify({"error":"str(e)error generating response || " + str(e)})
