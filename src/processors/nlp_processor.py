# src/processors/nlp_processor.py
import spacy
import re
from typing import List, Dict
import logging
from tqdm import tqdm

class NLPProcessor:
   def __init__(self, model: str = "en_core_web_sm"):
       try:
           self.nlp = spacy.load(model)
           self.nlp.max_length = 2000000  # Increase max length
       except OSError:
           import subprocess
           subprocess.run(["python", "-m", "spacy", "download", model])
           self.nlp = spacy.load(model)

   def process_text(self, text: str, max_definitions: int = 100) -> List[Dict[str, str]]:
       try:
           # Process text in chunks
           chunk_size = 100000
           terms_definitions = []
           
           for i in range(0, len(text), chunk_size):
               chunk = text[i:i+chunk_size]
               doc = self.nlp(chunk)
               
               for sent in doc.sents:
                   if len(terms_definitions) >= max_definitions:
                       return terms_definitions[:max_definitions]
                       
                   terms = self._extract_terms(sent)
                   terms_definitions.extend(terms)
                   
           return terms_definitions[:max_definitions]
           
       except Exception as e:
           logging.error(f"NLP processing error: {str(e)}")
           return []
           
   def _extract_terms(self, doc) -> List[Dict[str, str]]:
       terms = []
       for token in doc:
           if token.dep_ == "nsubj" and token.head.lemma_ in ["be", "mean", "refer"]:
               definition_tokens = [t for t in token.head.children if t.dep_ == "attr"]
               if definition_tokens:
                   terms.append({
                       "term": token.text,
                       "definition": " ".join(t.text for t in definition_tokens)
                   })
       return terms