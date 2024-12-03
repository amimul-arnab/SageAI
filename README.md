# SageAI Dataset Generator

AI-powered tool that simplifies complex terms into easier-to-understand definitions. Perfect for creating educational datasets from technical documents.

## Quick Start (3 Steps)

1. Clone the repository:
```bash
git clone https://github.com/amimul-arnab/SageAIDatasetGenerator.git
cd SageAIDatasetGenerator
```

2. Run setup (one-time setup only):
```bash
chmod +x setup.sh
./setup.sh
```

3. Run the application:
```bash
./run.sh
```

Access the web interface at http://127.0.0.1:5001

## Features
- PDF, DOCX, PPTX, and image file processing
- Automatic term and definition extraction
- AI-powered text simplification
- Export to CSV and JSON formats
- Progress tracking and detailed logging

## System Requirements
- Python 3.9 or higher
- Mac/Linux OS (Windows setup requires different commands)
- At least 2GB free disk space (for model and dependencies)
- 4GB RAM recommended

## Detailed Setup Guide

### Manual Setup (if automatic setup fails)
1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create required directories:
```bash
mkdir -p uploads output ~/.cache/gpt4all
```

### Model Information
The application uses GPT4All for text simplification. On first run, it will automatically download the required model (~1.5GB) to:
- Linux/Mac: ~/.cache/gpt4all/
- Windows: %USERPROFILE%\.cache\gpt4all\

## Usage Guide

### Web Interface
1. Access http://127.0.0.1:5001
2. Upload your document (PDF, DOCX, PPTX, or image)
3. Set maximum definitions to extract (default: 100)
4. Click "Process"
5. Download generated CSV and JSON files

### Supported File Types
- PDF (.pdf)
- Word Documents (.docx)
- PowerPoint Presentations (.pptx)
- Excel/CSV (.xlsx, .csv)
- Images (.jpg, .jpeg, .png)

### File Size Limits
- Maximum file size: 250MB
- Recommended file size: <50MB for optimal processing

## Output Format

### CSV Output
The generated CSV file includes:
- Term
- Original Definition
- Simplified Definition
- Analogy
- Mind Map Concepts

### JSON Output
Structured JSON format with the same information, suitable for API integration.

## Troubleshooting Guide

### Common Issues and Solutions

1. Setup Script Fails
```bash
# Try running each step manually
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Model Download Issues
- Manual download: Visit [GPT4All](https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin)
- Place in ~/.cache/gpt4all/ directory

3. OCR (Image Processing) Issues
```bash
# Mac
brew install tesseract

# Linux
sudo apt-get install tesseract-ocr
```

### Error Codes
- 400: Invalid file type or size
- 404: Resource not found
- 500: Processing error (check logs)

## Development and Contribution

### Project Structure
```
SageAIDatasetGenerator/
├── src/
│   ├── ai/
│   ├── extractors/
│   ├── processors/
│   ├── utils/
│   └── main.py
├── uploads/
├── output/
├── setup.sh
├── run.sh
└── requirements.txt
```

### Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Support
- Create an issue for bugs
- Check existing issues before reporting
- Include system info and error logs in reports

## Credits
- GPT4All for AI model
- Tesseract for OCR
- Various Python libraries (see requirements.txt)
