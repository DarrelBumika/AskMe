"""LLM service module for handling AI interactions."""

from pathlib import Path
from langchain_openai import ChatOpenAI
import getpass
from os import getenv, environ
from dotenv import load_dotenv
from typing import Optional


class ModelService:
    """Service class for managing LLM interactions."""

    def __init__(self, model: str = "arcee-ai/trinity-large-preview:free"):
        """Initialize the LLM service.

        Args:
            model: The model to use for LLM interactions.
        """
        # Load environment variables from .env file if it exists
        load_dotenv()

        if not getenv("OPENROUTER_API_KEY"):
            environ["OPENROUTER_API_KEY"] = getpass.getpass(
                "Enter your OpenRouter API key: "
            )

        self.model = model
        self._llm: Optional[ChatOpenAI] = None

    @property
    def llm(self) -> ChatOpenAI:
        """Lazily initialize and return the LLM instance."""
        if self._llm is None:
            self._llm = ChatOpenAI(
                model=self.model,
                stream_usage=True,
                base_url="https://openrouter.ai/api/v1",
                api_key=getenv("OPENROUTER_API_KEY"),
                temperature=0,
            )
        return self._llm

    @property
    def load_context(self) -> str:
        """Load context data for the LLM.

        Returns:
            The context data as a string.
        """
        try:
            # Get the directory of the current module and build the path to aboutme.txt
            module_dir = Path(__file__).parent.parent
            context_file = module_dir / "data" / "aboutme.txt"
            with open(context_file, "r") as file:
                context_data = file.read()
            return context_data
        except FileNotFoundError:
            return "No context available."

    def get_response(self, user_input: str, system_prompt: Optional[str] = None) -> str:
        """Get a response from the LLM.

        Args:
            user_input: The user's input text.
            system_prompt: Optional custom system prompt.

        Returns:
            The LLM's response.

        Raises:
            ValueError: If API configuration is invalid.
            Exception: If an error occurs during invocation.
        """
        try:
            default_prompt = (
                f"""
                You are a helpful assistant and helping user with FAQ. 
                Answer the user's question concisely using provided knowledge.
                If you don't know the answer, just say that you don't know,
                
                knowledge: {self.load_context}
                """
            )
            messages = [
                ("system", system_prompt or default_prompt),
                ("human", user_input),
            ]
            ai_msg = self.llm.invoke(messages)
            print(messages)
            return ai_msg.content
        except ValueError as e:
            raise ValueError(f"Configuration Error: {e}")
        except Exception as e:
            raise Exception(f"Error invoking LLM: {e}")

if __name__ == "__main__":
    service = ModelService()
    print(service.load_context)