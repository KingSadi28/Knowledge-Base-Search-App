from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from models import DocumentPhrase, SearchResult

class SemanticSearch:
    def __init__(self):
        # Same model as ingestion (must match!)
        print("Loading search model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Search ready!")
    
    def search(self, query: str, phrases: List[DocumentPhrase], top_k: int = 3) -> List[SearchResult]:
        # No phrases to search
        if not phrases:
            return []
        
        # Convert question to vector
        query_vector = self.model.encode(query)
        
        # Compare with all phrases
        results = []
        for phrase in phrases:
            phrase_vector = np.array(phrase.embedding)
            
            # Calculate similarity (how close the vectors are)
            similarity = np.dot(query_vector, phrase_vector) / (
                np.linalg.norm(query_vector) * np.linalg.norm(phrase_vector)
            )
            
            results.append(SearchResult(
                text=phrase.text,
                source=phrase.source,
                score=float(similarity)
            ))
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x.score, reverse=True)
        
        # Return top K results
        return results[:top_k]