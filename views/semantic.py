from langchain_openai import OpenAIEmbeddings
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
from langchain_postgres.vectorstores import PGVector
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from utils.custom_message_converter import MessageConverterWithDateTime
from langchain_ollama import OllamaLLM

# Load environment variables
load_dotenv()

# Connection string for PGVector
CONNECTION_STRING = "postgresql+psycopg2://postgres:postgres@localhost:5432/vector_db"


def run_agent_with_pgvector(user_input: str, user_id: str, max_number_of_messages: int):
    """
    Interact with the agent using LangChain, handle memory, and initialize document and message search.
    """
    # Initialize embeddings and vector store
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    db = PGVector(
        embeddings=embeddings,
        connection=CONNECTION_STRING,
        collection_name="articles",
    )

    # Initialize message history
    chat_history_table = "chat_messages"
    message_history = SQLChatMessageHistory(
        session_id=user_id,
        connection_string=CONNECTION_STRING,
        table_name=chat_history_table,
        custom_message_converter=MessageConverterWithDateTime(chat_history_table),
    )

    # Initialize buffer memory
    memory = ConversationBufferWindowMemory(
        chat_memory=message_history,
        memory_key="chat_history",
        return_messages=True,
        k=int(max_number_of_messages),
    )

    # Define the document search tool
    def search_document_tool(query: str):
        """
        Searches for a document based on the query input and returns similar results.
        """
        try:
            if not isinstance(query, str) or not query.strip():
                return "Query must be a valid non-empty string."
            similar_documents = db.similarity_search_with_score(query, k=5)
            return similar_documents if similar_documents else "No relevant documents found."
        except Exception as e:
            return f"Error searching for document: {str(e)}"

    # Initialize tools
    document_search = Tool(
        name="Document Search",
        func=search_document_tool,
        description="Search for documents related to the user's query.",
    )

    # Initialize the LLM and agent
    llm = OllamaLLM(model="deepseek-v2")
    agent = initialize_agent(
        tools=[document_search],
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
    )

    # Interact with the agent
    try:
        response = agent.invoke({"input": user_input})
        return response["output"]
    except Exception as e:
        return f"Error interacting with the agent: {str(e)}"
