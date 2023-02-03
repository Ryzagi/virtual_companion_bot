from pathlib import Path

from langchain import LLMChain
from langchain.chains import load_chain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.llms import OpenAI

from converbot.constants import CONVERSATION_SAVE_DIR, DEFAULT_FRIENDLY_TONE
from converbot.info_handler import ConversationToneHandler
from converbot.prompt import ConversationPrompt


class GPT3Conversation:
    """
    A conversation with a GPT-3 chatbot.

    Args:
        prompt: The prompt for the conversation.
        verbose: Whether to print verbose output.
        summary_buffer_memory_max_token_limit: The maximum number of tokens to store in the summary buffer memory.
    """

    def __init__(
        self,
        prompt: ConversationPrompt,
        verbose: bool = False,
        summary_buffer_memory_max_token_limit: int = 500,
    ):
        self._prompt = prompt
        self._language_model = OpenAI()
        self._memory = ConversationSummaryBufferMemory(
            llm=self._language_model,
            max_token_limit=summary_buffer_memory_max_token_limit,
            input_key=self._prompt.user_input_key,
            memory_key=self._prompt.memory_key,
            human_prefix=self._prompt.user_name,
            ai_prefix=self._prompt.chatbot_name,
        )
        self._conversation = LLMChain(
            llm=self._language_model,
            memory=self._memory,
            prompt=self._prompt.prompt,
            verbose=verbose,
        )

        self._tone_processor = ConversationToneHandler()
        self._tone = DEFAULT_FRIENDLY_TONE

    def set_tone(self, tone: str) -> None:
        """
        Set the tone of the chatbot.

        Args:
            tone: The tone of the chatbot.

        Returns: None
        """
        self._tone = self._tone_processor(tone)

    def ask(self, user_input: str) -> str:
        """
        Ask the chatbot a question and get a response.

        Args:
            user_input: The question to ask the chatbot.

        Returns: The response from the chatbot.
        """
        return self._conversation.predict(
            **{
                self._prompt.user_input_key: user_input,
                self._prompt.conversation_tone_key: self._tone,
                self._prompt.memory_key: self._memory,
            },
        )

    def serialize(
        self, chatbot_name: str, serialize_dir: Path = CONVERSATION_SAVE_DIR
    ) -> None:
        """
        Serialize the chatbot to disk.

        Args:
            serialize_dir: The directory to serialize the chatbot to.
            chatbot_name: The name of the chatbot.
        """
        serialize_dir.mkdir(exist_ok=True)
        self._conversation.save(
            (serialize_dir / chatbot_name).with_suffix(".json")
        )

    def load(
        self, chatbot_name: str, serialize_dir: Path = CONVERSATION_SAVE_DIR
    ) -> None:
        """
        Load a chatbot from disk.

        Args:
            serialize_dir: The directory to load the chatbot from.
            chatbot_name: The name of the chatbot.
        """
        self._conversation = load_chain(
            (serialize_dir / chatbot_name).with_suffix(".json")
        )
