"""Textual UI components for the AskMe application."""

from textual.app import App, ComposeResult
from textual.widgets import Footer, Static, Input, RichLog
from textual.containers import Vertical, Horizontal
from textual.binding import Binding
from src.core.chatbot import ChatBot


class AskMeApp(App[None]):
    """A Textual app for a terminal-based FAQ chatbot."""

    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle dark mode"),
        Binding("q", "action_quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.chatbot = ChatBot()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with Vertical(id="app-container"):
            with Horizontal(id="header-container"):
                yield Static("AskMe", id="title")
                yield Static("-", id="title-separator")
                yield Static("Ask everything about me", id="tagline")

            self.chat_log = RichLog(id="chat-log", markup=True)
            yield self.chat_log

            yield Input(id="question-input", placeholder="Type your question here...")

        yield Footer(
            compact=True,
            show_command_palette=False
        )

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle user input submission."""
        user_input = event.value.strip()
        input_widget = self.query_one("#question-input", Input)

        if user_input:
            # Display user message
            self.chat_log.write(
                f"[bold][#89986D]>[/#89986D] [#F6F0D7]{event.value}[/#F6F0D7][/bold]"
            )

            # Get response
            response = self.chatbot.get_response(user_input)
            self.chat_log.write(f"[italic #F6F0D7]{response}[/italic #F6F0D7]\n")

            # Clear input
            input_widget.value = ""

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
