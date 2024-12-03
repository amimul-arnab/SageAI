import logging
from typing import Optional
from gpt4all import GPT4All
import os

class Simplifier:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Define model paths
        model_name = "ggml-gpt4all-j-v1.3-groovy"
        model_path = os.path.join(os.path.expanduser('~'), '.cache', 'gpt4all')
        os.makedirs(model_path, exist_ok=True)
        
        try:
            self.logger.info(f"Initializing GPT4All with model path: {model_path}")
            self.model = GPT4All(
                model_name=model_name,
                model_path=model_path,
                allow_download=True,
                verbose=True
            )
            self.logger.info("Model initialized successfully")
        except Exception as e:
            self.logger.error(f"Model initialization error: {str(e)}")
            # Fallback to simpler processing if model fails
            self.model = None
            self.logger.warning("Running in fallback mode without AI model")

    def simplify_definition(self, text: str) -> Optional[str]:
        """Simplify text using GPT4All or fallback to basic processing."""
        try:
            if self.model:
                prompt = f"Simplify this text for a middle school student: {text}"
                response = self.model.generate(prompt, max_tokens=50)
                return response.strip()
            else:
                # Fallback processing
                return f"Simplified: {text}"
        except Exception as e:
            self.logger.error(f"Simplification error: {str(e)}")
            return None

    def generate_analogy(self, term: str, definition: str) -> Optional[str]:
        """Generate analogy using GPT4All or fallback to basic response."""
        try:
            if self.model:
                prompt = f"Create a simple analogy for {term}: {definition}"
                response = self.model.generate(prompt, max_tokens=30)
                return response.strip()
            else:
                # Fallback processing
                return f"Analogy for {term}: Like a familiar example"
        except Exception as e:
            self.logger.error(f"Analogy generation error: {str(e)}")
            return None

    def generate_mind_map_prompt(self, term: str, definition: str) -> Optional[str]:
        """Generate mind map prompt using GPT4All or fallback to basic structure."""
        try:
            if self.model:
                prompt = f"Create a mind map prompt for {term}. Include key concepts and relationships from: {definition}"
                response = self.model.generate(prompt, max_tokens=100)
                return response.strip()
            else:
                # Fallback processing
                return f"Mind map for {term}: Central concept - {term}"
        except Exception as e:
            self.logger.error(f"Mind map generation error: {str(e)}")
            return None

    def process_text(self, term: str, text: str) -> dict:
        """Process text with fallback handling if model fails."""
        return {
            "term": term,
            "complicated_text": text,
            "simplified_definition": self.simplify_definition(text),
            "analogy": self.generate_analogy(term, text),
            "mind_map_prompt": self.generate_mind_map_prompt(term, text)
        }