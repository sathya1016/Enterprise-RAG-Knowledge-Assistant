
from app.services.answer_generation import answer_generation_service


class ChatService:
    def __init__(self):
        self.answer_service = answer_generation_service

    def chat(
        self,
        message: str,
        document_id: str,
        top_k: int = 4,
        history: list | None = None,
    ):
        return self.answer_service.generate_chat_response(
            message=message,
            document_id=document_id,
            top_k=top_k,
            history=history,
        )


chat_service = ChatService()
