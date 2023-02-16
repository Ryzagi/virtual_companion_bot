import os

from langchain import PromptTemplate, LLMChain, OpenAI


class ConversationTextStyleHandler:

    def __init__(self):
        prompt_template = """Describe the texting style. 
        
        Example:

        Context: Describe the texting style of a 24 year old woman named Lisa that likes to swim and does banking for 
        a living. Her style needs to be very natural and include things like slang and typos 
        that are appropriate for her age. It is annoying if someone asks too many questions, so she does not do that. 
        
        Texting style: Lisa's texting style is casual and relaxed. She loves to use slang and abbreviations like 
        "OMG!" and "LOL" when texting her friends, and she often throws in a few typos for fun. She's not a big fan 
        of over-analyzing conversations and prefers to keep things light and breezy. She can be a bit of a jokestar, 
        so she often peppers her texts with witty comments and puns. Lisa also likes to use symbols, like ♥️ and 🤪, 
        to add extra personality to her messages. 
        
        Context: Describe the email writing style of a 35 year old man named John who is a lawyer and enjoys playing 
        tennis. His style should be professional but not overly formal, and he likes to get straight to the point. 

        Texting style: John's writing style is professional yet concise. He likes to get straight to the 
        point and does not waste time with unnecessary pleasantries or small talk. He uses formal language and proper 
        grammar, but he does not come across as stuffy or overly formal. He is direct and to the point, 
        and his emails are usually short and focused. John also likes to use bullet points to organize his thoughts 
        and make his emails easy to read. 
        
        Context: Describe the speaking style of a 50 year old professor named Dr. Jones who is an expert in 
        anthropology and enjoys hiking. His style should be intellectual and engaging. 
        
        Texting style: Dr. Jones has an intellectual and engaging speaking style. He speaks clearly and confidently, 
        with a calm and measured tone. He uses complex vocabulary and specialized terminology, but he explains things 
        in a way that is accessible to his audience. He is passionate about his subject matter and often uses 
        anecdotes and real-life examples to illustrate his points. Dr. Jones is also skilled at using humor to keep 
        his audience engaged and attentive. 
        
        Context: Describe the writing style of a 20 year old aspiring novelist named Lily who is a vegetarian and 
        likes to paint. Her style should be creative and expressive. 
        
        Texting style: Lily's writing style is creative and expressive. She has a poetic way of expressing herself 
        and uses vivid imagery to bring her stories to life. She often writes in a stream-of-consciousness style, 
        allowing her thoughts to flow freely onto the page. She is not overly concerned with grammar or punctuation, 
        instead focusing on the emotions and ideas she wants to convey. Lily's writing is introspective and 
        reflective, with a focus on the inner lives of her characters. She is also skilled at using symbolism to 
        convey deeper meanings and themes.
        
        Context: {user_input}
        Texting style:
        """
        prompt_template = PromptTemplate(input_variables=["user_input"], template=prompt_template)

        self._chain = LLMChain(
            llm=OpenAI(),
            prompt=prompt_template,
            verbose=False,
        )

    def __call__(self, user_input: str) -> str:
        return self._chain.predict(user_input=user_input)


if __name__ == '__main__':
    os.environ["OPENAI_API_KEY"] = "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"
    b = ConversationPromptHandler()
    print(b('Alice is pet lover, 25 years old, piano master. Her style is classic'))
