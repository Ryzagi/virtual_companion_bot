from pathlib import Path

CONVERSATION_SAVE_DIR = (
    Path(__file__).parent.parent / "database" / "saved_conversations"
)
HISTORY_SAVE_DIR = Path(__file__).parent.parent / "database" / "chat_history"

TIME, USER_MESSAGE, CHATBOT_RESPONSE = (
    "time",
    "user_message",
    "chatbot_response",
)

DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config" / "default.json"
DEFAULT_FRIENDLY_TONE = "The interlocutors share a friendly atmosphere, conversing easily and with a sense of mutual understanding."