from langchain_ollama import OllamaLLM
from langchain.memory import SQLChatMessageHistory, ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.utilities import SerpAPIWrapper
from sqlalchemy import create_engine

# PostgreSQL connection details
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/vector_db"

# Connect to PostgreSQL
engine = create_engine(DATABASE_URL)

# Setup SQL-based chat message history
session_id = "user_session_1"  # Unique ID per session
chat_history_table = "chat_messages"
message_history = SQLChatMessageHistory(
    session_id=session_id,
    connection_string=DATABASE_URL,
    table_name=chat_history_table,
    # custom_message_converter=MessageConverterWithDateTime(chat_history_table),
)

# Memory management
memory = ConversationBufferWindowMemory(
    chat_memory=message_history,
    memory_key="chat_history",
    return_messages=True,
    k=int(10),
)
# Initialize Ollama DeepSeek LLM
ollama_llm = OllamaLLM(model="deepseek-v2")


# Define a simple calculator tool
def simple_calculator(query: str) -> str:
    try:
        result = eval(query)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


calculator_tool = Tool(
    name="Simple Calculator",
    func=simple_calculator,
    description="Useful for performing basic math calculations. Input should be a mathematical expression."
)

# Initialize agent with LLM, memory, and tools
agent = initialize_agent(
    tools=[calculator_tool],
    llm=ollama_llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

# Example interactions
response_1 = agent.invoke({"input": "What is 25 * 4?"})
print(response_1)

response_2 = agent.invoke({"input": "What did I ask you earlier?"})
print(response_2)

response_3 = agent.invoke({"input": "What's the latest news about AI?"})
print(response_3)

response_4 = agent.invoke({"input": "Summarize our conversation so far."})
print(response_4)
