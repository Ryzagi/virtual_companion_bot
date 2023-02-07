from langchain import PromptTemplate, LLMChain, OpenAI


class ConversationToneHandler:

    def __init__(self):
        prompt_template = """Summarize person's tone for the conversation.
        
        Example:
        
        Context: be more prickly
        Conversation tone: sarcastic and prickly
        
        Context: make her happy
        Conversation tone: happy
        
        Context: fell in love very much
        Conversation tone: lovefully
        
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