from src.services.model_service import ModelService

class ChatBot:
    def __init__(self):
        self.model_service = ModelService()

    def get_response(self, user_input: str) -> str:
        """Get a response from the LLM.

        Args:
            user_input: The user's input text.

        Returns:
            The LLM's response.
        """

        return self.model_service.get_response(user_input)