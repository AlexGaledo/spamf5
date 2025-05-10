from google.genai import types
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
key = os.environ.get("gemini_key")
client = genai.Client(api_key=key)

# for itenary planner
def getChatbotResponse(user_input,sysin,location):
    if location is None: location = "not specified"
    try:
        prompt = f'{user_input}\n\nPreferred Location: {location}'
        response = client.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt],
            generation_config=types.GenerationConfig(candidate_count=1),
            system_instruction=sysin
        )
        textResponse = response.text


        return {"response":textResponse,"location":location}
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")  
        return {"response": f"An error occurred: {str(e)}", "location": location}
