from pydantic import BaseModel

class Chat(BaseModel):
    """
    Chatbot
    """
    session_id: str
    prompt: str