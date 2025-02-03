# Semantic Document Search

This project implements a semantic document search using LangChain, PGVector, and Flask. It allows users to search for documents based on their queries and interact with an agent that uses a conversational model.

## Features

- **Semantic Search**: Uses OpenAI embeddings and PGVector for document similarity search.
- **Conversational Agent**: Utilizes LangChain and OllamaLLM for conversational interactions.
- **Flask API**: Provides endpoints for document search requests.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/semantic-document-search.git
    cd semantic-document-search
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    Create a `.env` file in the root directory and add the following:
    ```env
    DEBUG_MODE=True
    APPLICATION_HOST=127.0.0.1
    APPLICATION_PORT=3000
    APPLICATION_APPLICATION_ROOT=""
    APP_LOG=app.log
    ```

## Setting Up the Database

1. **Install PostgreSQL**: Make sure you have PostgreSQL installed on your system. You can download it from [here](https://www.postgresql.org/download/).

2. **Create a Database**: Create a new database named `vector_db`:
    ```sh
    psql -U postgres -c "CREATE DATABASE vector_db;"
    ```

3. **Create Tables**: Use the following SQL commands to create the necessary tables for storing document embeddings and chat messages:
    ```sql
    CREATE TABLE articles (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding VECTOR(1536) -- Adjust the dimension according to your embedding model
    );

    CREATE TABLE chat_messages (
        id SERIAL PRIMARY KEY,
        session_id VARCHAR(255),
        message TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

4. **Set Up Connection String**: Ensure your connection string in `views/semantic.py` is correctly configured:
    ```python
    CONNECTION_STRING = "postgresql+psycopg2://username:password@localhost:5432/db_name"
    ```

## Usage

1. Start the Flask application:
    ```sh
    python main.py
    ```

2. The application will be running at `http://127.0.0.1:3000`.

3. Use the `/document/search` endpoint to search for documents. Example request:
    ```sh
    curl -X POST http://127.0.0.1:3000/document/search -H "Content-Type: application/json" -d '{"query": "your search query", "user_id": "user123", "max_messages": 5}'
    ```

## Project Structure

- `main.py`: Entry point for the Flask application.
- `config.py`: Configuration settings for the application.
- `routes/semantic.py`: Defines the Flask routes for document search.
- `views/semantic.py`: Contains the logic for interacting with LangChain and PGVector.

## LangChain

LangChain is a framework designed to facilitate the development of applications that use large language models (LLMs). It provides tools and abstractions to manage the interaction with LLMs, making it easier to build complex applications that require natural language understanding and generation. LangChain supports various LLMs and offers features like memory management, tool integration, and agent initialization.

## Agents in LangChain

Agents in LangChain are components that can perform tasks based on user input. They can be initialized with specific tools and memory configurations to handle different types of interactions. Agents can be conversational, allowing them to maintain context over multiple interactions, and can use various LLMs to generate responses.

## DeepSeek with Ollama

DeepSeek is a conversational model provided by Ollama, which is integrated into LangChain as an LLM. It is designed to handle complex queries and provide meaningful responses. By using DeepSeek with LangChain, developers can create applications that leverage advanced conversational capabilities, enabling more natural and effective interactions with users.

## Setting Up Local DeepSeek with Ollama

To set up a local instance of DeepSeek from Ollama, follow these steps:

1. **Install Ollama**: First, you need to install the Ollama package.

2. **Download DeepSeek Model**: You need to download the DeepSeek model. This can be done using the Ollama CLI or API. Ensure you have the necessary permissions and access to the model.

3. **Configure Ollama**: Set up the configuration for Ollama to use the DeepSeek model. This might involve setting environment variables or configuration files.

4. **Integrate with LangChain**: Ensure that your LangChain setup is configured to use the local instance of DeepSeek. This involves specifying the model and any necessary parameters.

For detailed instructions, refer to this [article](https://dev.to/ajmal_hasan/setting-up-ollama-running-deepseek-r1-locally-for-a-powerful-rag-system-4pd4).

Here is an example of how you might configure and use the DeepSeek model locally in your `views/semantic.py` file:

```python
from langchain_ollama import OllamaLLM

# Initialize the LLM with the local DeepSeek model
llm = OllamaLLM(model="deepseek-v2", local=True)

# Use the LLM in your agent initialization
agent = initialize_agent(
    tools=[document_search],
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
)