from pydantic import BaseModel
from typing import Optional

class SearchParams(BaseModel):
    query: Optional[str] = None
    max_results: int = 10  # facultatif, valeur par défaut : 10
    assurance: Optional[str] = None  # "1", "2", "nc"
    location: str  # requis
