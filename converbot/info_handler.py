from langchain import PromptTemplate, LLMChain, OpenAI


class ConversationToneHandler:

    def __init__(self):
        prompt_template = """Summarize and paraphrase user context for conversation, to set the tone for the conversation.
        
        Example:
        
        Context: mood sarcastic
        Conversation tone: The dialogue becomes sarcastic, distrust grows between the interlocutors.
        
        Context: its rainy outside
        Conversation tone: Rain is heard outside the window, the sky is covered with clouds, the interlocutors are a little interrupted by the sound of drops.
        
        Context: love
        Conversation tone: A spark passes between the interlocutors, and it seems that they have fallen in love.
        
        Context: {user_input}
        Conversation tone:
        """
        prompt_template = PromptTemplate(input_variables=["user_input"], template=prompt_template)

        self._chain = LLMChain(
            llm=OpenAI(),
            prompt=prompt_template,
            verbose=False,
        )

    def __call__(self, user_input: str) -> str:
        return self._chain.predict(user_input=user_input)