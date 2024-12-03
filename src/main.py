import os
import sys
import logging
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from src.utils.file_validator import validate_file
from src.extractors.text_extractor import TextExtractor
from src.processors.nlp_processor import NLPProcessor
from src.ai.simplifier import Simplifier
from src.output.data_writer import DataWriter

# Initialize Flask app
app = Flask(__name__, 
   template_folder=os.path.join(project_root, 'templates'),
   static_folder=os.path.join(project_root, 'static'))

# Add CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Configure logging
app.logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Configure upload handling
UPLOAD_FOLDER = os.path.join(project_root, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 250 * 1024 * 1024  # 250MB max-length

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST', 'OPTIONS'])
def upload_file():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
        
    if request.method == 'GET':
        return jsonify({'status': 'ready'})

    app.logger.info(f"Upload request received - Method: {request.method}")
    app.logger.info(f"Files: {request.files}")
    app.logger.info(f"Form data: {request.form}")

    if 'file' not in request.files:
        app.logger.error("No file in request")
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        app.logger.error("Empty filename")
        return jsonify({'error': 'No file selected'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        app.logger.info(f"Saving file to: {filepath}")
        file.save(filepath)

        # Validate file
        app.logger.info("File saved successfully, validating...")
        valid, message = validate_file(filepath)
        if not valid:
            app.logger.error(f"File validation failed: {message}")
            return jsonify({'error': message}), 400

        # Extract text
        app.logger.info("File validated, extracting text...")
        extractor = TextExtractor()
        text = extractor.extract(filepath)
        if not text:
            app.logger.error("Text extraction failed")
            raise ValueError("Text extraction failed")

        # Process with NLP
        app.logger.info("Processing text with NLP...")
        processor = NLPProcessor()
        terms_defs = processor.process_text(text)
        
        # Process with GPT4ALL
        app.logger.info("Processing with AI simplifier...")
        simplifier = Simplifier()
        dataset = []
        for item in terms_defs:
            processed = simplifier.process_text(item['term'], item['definition'])
            dataset.append(processed)

        # Save output files
        app.logger.info("Saving output files...")
        output_dir = os.path.join(project_root, 'output')
        os.makedirs(output_dir, exist_ok=True)

        base_name = Path(filename).stem
        csv_path = os.path.join(output_dir, f"{base_name}_dataset.csv")
        json_path = os.path.join(output_dir, f"{base_name}_dataset.json")

        writer = DataWriter()
        csv_success = writer.save_csv(dataset, csv_path)
        json_success = writer.save_json(dataset, json_path)

        if not (csv_success and json_success):
            raise ValueError("Failed to save output files")

        app.logger.info("Processing complete!")
        return jsonify({
            'message': 'Processing complete',
            'csv_path': csv_path,
            'json_path': json_path,
            'terms_processed': len(dataset)
        })

    except Exception as e:
        app.logger.error(f"Processing error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

    finally:
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
            app.logger.info(f"Cleaned up temporary file: {filepath}")

if __name__ == '__main__':
    app.logger.info(f"Server starting. Project root: {project_root}")
    app.run(debug=True, host='0.0.0.0', port=5001)