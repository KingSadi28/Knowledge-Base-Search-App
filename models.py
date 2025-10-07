from dataclasses import dataclass
from typing import List

@dataclass
class DocumentPhrase:
    text: str           # The actual text
    source: str        # Which file it came from
    phrase_id: int       # Position in the document
    embedding: List[float] # The embedding (numbers representing meaning)

@dataclass
class SearchResult:
    text: str           # The relevant text found
    source: str        # Which document it's from
    score: float        # How relevant it is (0-1)