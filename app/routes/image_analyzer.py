from flask import Blueprint, request, jsonify
from services.vertex import generate_with_image
import os,boto3
from uuid import uuid4

analyzer_bp = Blueprint("/analyzer",__name__)

@analyzer_bp.route("/",methods=["POST","GET"])
def analyzeRequest():
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION')
    )

    #use user ID as key for authentication next time,
    # key = request.args.get('projectID')
    # if not key:
    #     return jsonify({'response' : 'need project id'}) 

    file = request.files.get('file')
    if not file:
        return jsonify({'response': 'requires uploaded file'})
    
    file_extension = file.filename.split('.')[-1].lower()
    s3_key = f'projects/{uuid4()}/preview.{file_extension}'
    bucket = 'akbai-bucket'
    try:
        s3.upload_fileobj(
            file,
            bucket,
            s3_key,
            ExtraArgs={'ACL': 'public-read'}  # <--- Make it publicly accessible
        )
        sysin_image = "Analyze this image"  
        url = f'https://{bucket}.s3.amazonaws.com/{s3_key}'

        response = generate_with_image(sysin_image, url)
        print("console debug:" + response)
        return jsonify({
            "response" : response
        })
    except Exception as e:
        return jsonify({'response':'error interacting with s3 storage', 'error': str(e)}), 500




 