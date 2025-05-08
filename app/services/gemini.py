from google.genai import types
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("gemini_key")
client = genai.Client(api_key=key)

# for itenary planner
def getChatbotResponse(user_input,sysin,location):
    if location is None: location = "not specified"
    try:
        prompt = f'{user_input}\n\nPreferred Location: {location}'
        response =client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=sysin),
            contents = [{"role":"user","parts":[prompt]}]
        )
        textResponse = response.text

        return {"response":textResponse,"location":location}
    
    except Exception as e:
        return {"response": "An error occurred while generating the response.", "location": location}
