from textual.app import App, ComposeResult
from textual.widgets import Footer, Static, Input, RichLog
from textual.containers import Vertical, Horizontal
from textual.binding import Binding


class AskMe(App[None]):
    """A Textual app for a terminal-based FAQ chatbot."""

    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle dark mode"),
        Binding("q", "quit", "Quit"),
    ]

    # Simple FAQ knowledge base
    FAQ = {
        "hello": "Hello! How can I help you today?",
        "hi": "Hello! How can I help you today?",
        "name": "My name is Ashilpa Darrel Bumika, a software developer and tech enthusiast.",
        "education": "I hold a Bachelor's degree in Engineering (Information Technology) from Universitas Negeri Yogyakarta.",
    }

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
            self.chat_log.write(f"[bold][#89986D]>[/#89986D] [#F6F0D7]{event.value}[/#F6F0D7][/bold]")

            # Get response
            response = self.get_response(user_input)
            self.chat_log.write(f"[italic #F6F0D7]{response}[/italic #F6F0D7]\n")

            # Clear input
            input_widget.value = ""

    def get_response(self, user_input: str) -> str:
        """Generate a response based on user input."""
        user_input_lower = user_input.lower()

        # Check for exact matches
        if user_input_lower in self.FAQ:
            return self.FAQ[user_input_lower]

        # Check for keywords
        for keyword, response in self.FAQ.items():
            if keyword != "default" and keyword in user_input_lower:
                return response

        # Default response
        return self.FAQ["default"]

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = AskMe()
    app.run()