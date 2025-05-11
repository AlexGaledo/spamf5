import os
from flask import Blueprint, request, jsonify
from services.vertex import generate_with_image

analyzer_bp = Blueprint("/analyzer", __name__)

@analyzer_bp.route("/", methods=["POST", "GET"])
def analyzeRequest():
    file = request.files.get('file')
    if not file:
        return jsonify({'response': 'requires uploaded file'}), 400

    try:
        temp_dir = "uploads"  #temp folder to save image 
        os.makedirs(temp_dir, exist_ok=True)
        filepath = os.path.join(temp_dir, file.filename)
        file.save(filepath)

        # Call Gemini function + System Instruction
        sysin = "Analyze this image"
        response = generate_with_image(sysin, filepath)

        return jsonify({"response": response}), 200

    except Exception as e:
        return jsonify({
            "response": "error occured",
            "error": str(e)
        }), 500
    
    finally:
        try: # Cleanup uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as cleanup_error:
            print(f"Cleanup failed: {cleanup_error}")
