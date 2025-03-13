from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
prompt= ChatPromptTemplate.from_messages([
    ("system"," your name is Amscart Bot. your work is to help a customer to buy a product. if you dont know answer say I din't know. your work is to sell the product your customer"),
    ("human"," {chat_history} based on history give your output thid question:    {human_input}")
])

llm = ChatGroq(model="llama-3.3-70b-versatile",api_key="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")
 

memory = ConversationBufferMemory(memory_key="chat_history")
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
)

