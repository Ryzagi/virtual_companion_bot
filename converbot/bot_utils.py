import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from converbot.config import RomanitcConversationConfig
from converbot.core import GPT3Conversation
from converbot.prompt import RomanticConversationPrompt


@dataclass
class ConversationContext:
    name: str
    age: str
    interests: str
    profession: str
    gender: str


def parse_context(message: str) -> Optional[ConversationContext]:
    """
    Parse context string and return it as ConversationContext object.

    Args:
        message: The context string.


    Returns:
        The ConversationContext object.
    """
    splitted_message = message.split(",")
    if len(splitted_message) != 5:
        return None
    else:
        name, age, interests, profession, gender = message.split(",")
        return ConversationContext(
            name=name,
            age=age,
            interests=interests,
            profession=profession,
            gender=gender,
        )


def create_conversation_from_context(
    context: ConversationContext,
    config_path: Path,
) -> GPT3Conversation:
    """
    Create a conversation from the context.

    Args:
        context: The context.

    Returns: The conversation.
    """
    print(context)
    config = RomanitcConversationConfig.from_json(config_path)
    conversation = GPT3Conversation(
        prompt=RomanticConversationPrompt(
            prompt_template=config.prompt_template,
            name=context.name,
            age=context.age,
            interests=context.interests,
            profession=context.profession,
            gender=context.gender,
        ),
        summary_buffer_memory_max_token_limit=config.summary_buffer_memory_max_token_limit,
    )
    return conversation


