from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class GraphState:
    question: str = ""
    retrieved_docs: List[Dict[str, Any]] = field(default_factory=list)
    answer: str = ""
    chat_history: List[Dict[str, str]] = field(default_factory=list)
