"""
LEPT AI Reviewer - Supabase PostgreSQL Database Connection
OPTIMIZED: Single cached connection, reused across all queries
"""

import streamlit as st
import psycopg2
import psycopg2.extras
from typing import Optional, List, Tuple
import time


def _increment_query_count():
    """Safely increment the query counter."""
    try:
        if "db_query_count" not in st.session_state:
            st.session_state.db_query_count = 0
        st.session_state.db_query_count += 1
    except Exception:
        pass


@st.cache_resource
def get_connection():
    """
    Create and cache a single Supabase PostgreSQL connection.
    This connection is reused across ALL reruns and users.
    """
    try:
        conn = psycopg2.connect(
            host=st.secrets["supabase"]["host"],
            port=st.secrets["supabase"].get("port", 5432),
            dbname=st.secrets["supabase"]["database"],
            user=st.secrets["supabase"]["user"],
            password=st.secrets["supabase"]["password"],
            sslmode="require",
            connect_timeout=30,
        )
        conn.autocommit = False
        return conn
    except Exception as e:
        st.error(f"Failed to connect to Supabase: {str(e)}")
        return None


def _get_valid_connection():
    """Get a valid connection, reconnecting if needed."""
    conn = get_connection()
    if conn is None:
        return None
    try:
        # Test if connection is still alive
        conn.poll()
        if conn.closed:
            st.cache_resource.clear()
            conn = get_connection()
    except Exception:
        try:
            conn.reset()
        except Exception:
            st.cache_resource.clear()
            conn = get_connection()
    return conn


def execute_query(query: str, params: tuple = None, fetch: bool = True) -> Optional[List]:
    """
    Execute a query using the cached connection.
    
    Args:
        query: SQL query string (use %s for parameters)
        params: Query parameters (optional)
        fetch: Whether to fetch results (default True)
    
    Returns:
        List of results if fetch=True, True if successful write, None on error
    """
    _increment_query_count()
    
    conn = _get_valid_connection()
    if conn is None:
        return None
    
    cursor = None
    try:
        start_time = time.time()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = True
        
        elapsed = (time.time() - start_time) * 1000
        if elapsed > 500:
            print(f"SLOW QUERY ({elapsed:.0f}ms): {query[:100]}...")
        
        return result
        
    except psycopg2.OperationalError as e:
        # Connection lost, try to reconnect once
        try:
            conn.rollback()
        except Exception:
            pass
        st.cache_resource.clear()
        try:
            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                if fetch:
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return True
        except Exception:
            pass
        return None
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print(f"Query error: {str(e)}")
        return None
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception:
                pass


def execute_write(query: str, params: tuple = None) -> bool:
    """Execute a write query (INSERT, UPDATE, DELETE)."""
    result = execute_query(query, params, fetch=False)
    return result is True


def test_connection() -> Tuple[bool, str]:
    """Test the database connection."""
    try:
        result = execute_query("SELECT version()")
        if result and len(result) > 0:
            return True, result[0][0]
        return False, "Connection test failed"
    except Exception as e:
        return False, str(e)


def get_query_count() -> int:
    """Get the number of queries executed in this session (for debugging)."""
    try:
        return st.session_state.get("db_query_count", 0)
    except Exception:
        return 0


def reset_query_count():
    """Reset the query counter (for debugging)."""
    try:
        st.session_state.db_query_count = 0
    except Exception:
        pass
