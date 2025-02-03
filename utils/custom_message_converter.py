from langchain_core.messages import (
    BaseMessage,
    message_to_dict,
    messages_from_dict,
)
from langchain_community.chat_message_histories.sql import BaseMessageConverter
from sqlalchemy.ext.declarative import declarative_base
from typing import Any
import json
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import Session


def create_message_model(table_name, DynamicBase):
    """
    Create a message model for a given table name.

    Args:
        table_name: The name of the table to use.
        DynamicBase: The base class to use for the model.

    Returns:
        The model class.

    """

    # Model declared inside a function to have a dynamic table name
    class Message(DynamicBase):
        __tablename__ = table_name
        id = Column(Integer, primary_key=True)
        session_id = Column(Text)
        message = Column(Text)
        created_at = Column(DateTime)

    return Message


class MessageConverterWithDateTime(BaseMessageConverter):
    """Custom message converter for SQLChatMessageHistory that store DateTime of messages in the DB."""

    def __init__(self, table_name: str):
        self.model_class = create_message_model(table_name, declarative_base())

    def from_sql_model(self, sql_message: Any) -> BaseMessage:
        """
        Convert a SQL model to a BaseMessage object.

        Args:
            sql_message (Any): The SQL model to convert.

        Returns:
            BaseMessage: The converted BaseMessage object.
        """
        return messages_from_dict([json.loads(sql_message.message)])[0]

    def to_sql_model(self, message: BaseMessage, session_id: str) -> Any:
        """
        Converts a given message and session ID into a SQL model object.

        Args:
            message (BaseMessage): The message to be converted.
            session_id (str): The session ID associated with the message.

        Returns:
            Any: The SQL model object representing the converted message.
        """
        current_time = datetime.now()
        return self.model_class(
            session_id=session_id,
            message=json.dumps(message_to_dict(message)),
            created_at=current_time,
        )

    def get_sql_model_class(self) -> Any:
        return self.model_class

    # A function that clears or delete the messages for the given date range for the specific session_id
    def clear_messages(
        self,
        session: Session,
        session_id: str,
        start_date: datetime,
        end_date: datetime,
    ):
        """
        Clears or deletes the messages for the given date range for the specific session_id.

        Args:
            session (Session): The SQLAlchemy session to use for database operations.
            session_id (str): The session ID to filter the messages.
            start_date (datetime): The start date of the range.
            end_date (datetime): The end date of the range.
        """
        # Creating the query
        query = session.query(self.model_class).filter(
            self.model_class.session_id == session_id,
            self.model_class.created_at.between(start_date, end_date),
        )
        # Executing the query
        query.delete(synchronize_session="fetch")
        session.commit()
