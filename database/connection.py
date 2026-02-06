"""
LEPT AI Reviewer - Snowflake Database Connection
"""

import streamlit as st
import snowflake.connector
from contextlib import contextmanager


def get_snowflake_connection():
    """
    Create and return a Snowflake connection using Streamlit secrets.
    """
    try:
        conn = snowflake.connector.connect(
            account=st.secrets["snowflake"]["account"],
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            role=st.secrets["snowflake"].get("role", "ACCOUNTADMIN"),
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"],
            warehouse=st.secrets["snowflake"]["warehouse"]
        )
        return conn
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {str(e)}")
        return None


@contextmanager
def get_db_cursor():
    """
    Context manager for database operations.
    Automatically handles connection and cursor cleanup.
    """
    conn = None
    cursor = None
    try:
        conn = get_snowflake_connection()
        if conn:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        else:
            yield None
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def execute_query(query: str, params: tuple = None, fetch: bool = True):
    """
    Execute a query and optionally fetch results.
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        fetch: Whether to fetch results (default True)
    
    Returns:
        List of results if fetch=True, otherwise None
    """
    with get_db_cursor() as cursor:
        if cursor is None:
            return None
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                return cursor.fetchall()
            return True
        except Exception as e:
            st.error(f"Query execution failed: {str(e)}")
            return None


def execute_many(query: str, params_list: list):
    """
    Execute a query with multiple parameter sets.
    
    Args:
        query: SQL query string
        params_list: List of parameter tuples
    
    Returns:
        True if successful, None otherwise
    """
    with get_db_cursor() as cursor:
        if cursor is None:
            return None
        
        try:
            cursor.executemany(query, params_list)
            return True
        except Exception as e:
            st.error(f"Batch execution failed: {str(e)}")
            return None


def test_connection():
    """
    Test the Snowflake connection.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        conn = get_snowflake_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT CURRENT_VERSION()")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return True, result[0]
        return False, "Connection failed"
    except Exception as e:
        return False, str(e)
