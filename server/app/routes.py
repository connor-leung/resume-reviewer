from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from .parser import parse_resume
from .pdf_parser import extract_text_from_pdf
from .scorer import score_resume

bp = Blueprint('api', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/api/parse_resume', methods=['POST'])
def parse_resume_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        resume_text = extract_text_from_pdf(filepath)

        job_description = request.form.get('job_description', '')
        job_type = request.form.get('job_type', '')  
        parsed_data = parse_resume(resume_text, job_type, job_description)
        score = score_resume(parsed_data, job_description, job_type) 

        return jsonify({
            "parsed_data": parsed_data,
            "score": score
        })
    else:
        return jsonify({"error": "Invalid file type"}), 400
