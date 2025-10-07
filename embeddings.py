from sentence_transformers import SentenceTransformer
from typing import List
from models import DocumentPhrase

class DocumentIngestion:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.phrases: List[DocumentPhrase] = []
        print("Loaded model!")

    def embed_documents(self, text: str, filename: str) -> int:
        # Step 1: Split text into chunks (same as before)
        words = text.split()
        chunk_size = 200
        overlap = 50
        
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk_text = ' '.join(words[i:i + chunk_size])
            
            chunk = DocumentPhrase(
                text=chunk_text,
                source=filename,
                phrase_id=i,
                embedding=[]
            )
            chunks.append(chunk)

        # Step 2: Generate embeddings for all chunks at once
        texts = [chunk.text for chunk in chunks]
        embeddings = [embedding.tolist() for embedding in self.model.encode(texts, convert_to_numpy=True)]
        
        # Step 3: Store chunks with their embeddings
        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding
            self.phrases.append(chunk)
    
        return len(chunks)
    
    def get_all_phrases(self) -> List[DocumentPhrase]:
        return self.phrases