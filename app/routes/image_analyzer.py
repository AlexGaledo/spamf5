from flask import Blueprint, request, jsonify
from services.vertex import generate_with_image


analyzer_bp = Blueprint("/analyzer",__name__)

@analyzer_bp.route("/",methods=["POST","GET"])
def analyzeRequest():
    
    file = request.files.get('file')
    if not file:
        return jsonify({'response': 'requires uploaded file'})
    
    try:
        sysin = "Analyze this image"
        response = generate_with_image(sysin,file)
        return jsonify({
            "response":response
        }), 200
    
    except Exception as e:
        return jsonify({
            "response":"error occured",
            "error":str(e)
        }), 500



    
    

    




 