from typing import TypedDict

class AgentState(TypedDict):
  topic: str
  instruction: str
  article: str
  review_message: str
  revision_message: str