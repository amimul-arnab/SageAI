import os
import logging
from typing import Tuple

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

ALLOWED_EXTENSIONS = {
    'pdf', 'docx', 'pptx', 'xlsx', 
    'csv', 'jpeg', 'jpg', 'png'
}

MAX_FILE_SIZE = 250 * 1024 * 1024  # 250MB

def validate_file(filepath: str) -> Tuple[bool, str]:
    """
    Validate file type and size.
    
    Args:
        filepath (str): Path to the file to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    try:
        logger.info(f"Starting validation for file: {filepath}")
        
        # Check if file exists
        if not os.path.exists(filepath):
            error_msg = f"File does not exist: {filepath}"
            logger.error(error_msg)
            return False, error_msg
            
        # Check file size
        file_size = os.path.getsize(filepath)
        logger.debug(f"File size: {file_size/1024/1024:.2f}MB")
        
        if file_size > MAX_FILE_SIZE:
            error_msg = f"File size ({file_size/1024/1024:.2f}MB) exceeds limit of {MAX_FILE_SIZE/1024/1024}MB"
            logger.error(error_msg)
            return False, error_msg
            
        # Check file extension
        if '.' not in filepath:
            error_msg = "No file extension found"
            logger.error(error_msg)
            return False, error_msg
            
        extension = filepath.rsplit('.', 1)[1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            error_msg = f"File type .{extension} not supported. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            logger.error(error_msg)
            return False, error_msg
            
        logger.info(f"File validation successful for {filepath}")
        return True, "File validation successful"
        
    except Exception as e:
        error_msg = f"Validation error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg